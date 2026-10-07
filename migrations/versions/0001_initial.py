"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("timezone", sa.String(64), nullable=True),
        sa.Column("is_onboarded", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("level", sa.String(2), nullable=True),
        sa.Column("dictionary_code", sa.String(64), nullable=True),
        sa.Column("words_per_lesson", sa.Integer(), nullable=False, server_default=sa.text("5")),
        sa.Column("daily_lesson_limit", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("last_lesson_number", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.CheckConstraint("email = lower(email)", name="ck_users_email_lower"),
        sa.CheckConstraint(
            "level IS NULL OR level IN ('A1','A2','B1','B2','C1','C2')",
            name="ck_users_level_valid",
        ),
        sa.CheckConstraint("words_per_lesson >= 1", name="ck_users_words_per_lesson_min"),
        sa.CheckConstraint("daily_lesson_limit >= 1", name="ck_users_daily_lesson_limit_min"),
        sa.CheckConstraint("last_lesson_number >= 0", name="ck_users_last_lesson_number_min"),
        sa.CheckConstraint(
            "NOT is_onboarded OR (timezone IS NOT NULL AND level IS NOT NULL AND dictionary_code IS NOT NULL)",
            name="ck_users_onboarded_fields",
        ),
    )

    # --- auth_sessions ---
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("token_hash", sa.String(128), nullable=False),
        sa.Column("csrf_token_hash", sa.String(128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_auth_sessions"),
        sa.UniqueConstraint("token_hash", name="uq_auth_sessions_token_hash"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="fk_auth_sessions_user_id_users"),
    )
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.create_index("ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"])

    # --- words ---
    op.create_table(
        "words",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("lemma", sa.String(64), nullable=False),
        sa.Column("lemma_key", sa.String(64), nullable=False),
        sa.Column("pos", sa.String(10), nullable=False),
        sa.Column("level", sa.String(2), nullable=True),
        sa.Column("translations", ARRAY(sa.String()), nullable=False),
        sa.Column("in_general", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("in_it", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("in_travel", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("id", name="pk_words"),
        sa.UniqueConstraint("lemma_key", "pos", name="uq_words_lemma_key_pos"),
        sa.CheckConstraint(
            "pos IN ('noun','verb','adj','adv','pron','prep','conj','num','det','intj')",
            name="ck_words_pos_valid",
        ),
        sa.CheckConstraint(
            "level IS NULL OR level IN ('A1','A2','B1','B2','C1','C2')",
            name="ck_words_level_valid",
        ),
        sa.CheckConstraint(
            "array_length(translations, 1) BETWEEN 1 AND 5",
            name="ck_words_translations_length",
        ),
        sa.CheckConstraint("char_length(lemma) BETWEEN 1 AND 64", name="ck_words_lemma_length"),
        sa.CheckConstraint("char_length(lemma_key) BETWEEN 1 AND 64", name="ck_words_lemma_key_length"),
    )
    op.create_index("ix_words_level_general", "words", ["level"], postgresql_where=sa.text("in_general = true"))
    op.create_index("ix_words_level_it", "words", ["level"], postgresql_where=sa.text("in_it = true"))
    op.create_index("ix_words_level_travel", "words", ["level"], postgresql_where=sa.text("in_travel = true"))

    # --- user_words ---
    op.create_table(
        "user_words",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("word_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(10), nullable=False, server_default=sa.text("'active'")),
        sa.Column("stage", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("due_lesson_number", sa.Integer(), nullable=True),
        sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_user_words"),
        sa.UniqueConstraint("user_id", "word_id", name="uq_user_words_user_word"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_words_user_id_users"),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE", name="fk_user_words_word_id_words"),
        sa.CheckConstraint(
            "status IN ('active','mastered','ignored')",
            name="ck_user_words_status_valid",
        ),
        sa.CheckConstraint("stage BETWEEN 0 AND 6", name="ck_user_words_stage_range"),
        sa.CheckConstraint(
            "due_lesson_number IS NULL OR due_lesson_number > 0",
            name="ck_user_words_due_positive",
        ),
        sa.CheckConstraint(
            "NOT (status = 'active' AND due_lesson_number IS NULL)",
            name="ck_user_words_active_has_due",
        ),
        sa.CheckConstraint(
            "NOT (status <> 'active' AND due_lesson_number IS NOT NULL)",
            name="ck_user_words_inactive_no_due",
        ),
    )
    op.create_index("ix_user_words_user_status_due", "user_words", ["user_id", "status", "due_lesson_number"])
    op.create_index(
        "ix_user_words_user_due_active",
        "user_words",
        ["user_id", "due_lesson_number"],
        postgresql_where=sa.text("status = 'active'"),
    )

    # --- lessons ---
    op.create_table(
        "lessons",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("lesson_number", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default=sa.text("'in_progress'")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("started_local_date", sa.Date(), nullable=False),
        sa.Column("completed_local_date", sa.Date(), nullable=True),
        sa.Column("gen_prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("gen_completion_tokens", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_lessons"),
        sa.UniqueConstraint("user_id", "lesson_number", name="uq_lessons_user_number"),
        sa.UniqueConstraint("user_id", "idempotency_key", name="uq_lessons_user_idempotency"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="fk_lessons_user_id_users"),
        sa.CheckConstraint("lesson_number > 0", name="ck_lessons_number_positive"),
        sa.CheckConstraint(
            "char_length(idempotency_key) BETWEEN 1 AND 128",
            name="ck_lessons_idempotency_key_length",
        ),
        sa.CheckConstraint(
            "status IN ('in_progress','completed')",
            name="ck_lessons_status_valid",
        ),
        sa.CheckConstraint(
            "NOT (status = 'completed' AND (completed_at IS NULL OR completed_local_date IS NULL))",
            name="ck_lessons_completed_fields",
        ),
        sa.CheckConstraint(
            "NOT (status = 'in_progress' AND (completed_at IS NOT NULL OR completed_local_date IS NOT NULL))",
            name="ck_lessons_in_progress_fields",
        ),
    )
    op.create_index("ix_lessons_user_started_date", "lessons", ["user_id", "started_local_date"])
    op.create_index("ix_lessons_user_completed_date", "lessons", ["user_id", "completed_local_date"])
    op.create_index(
        "uq_lessons_user_in_progress",
        "lessons",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'in_progress'"),
    )

    # --- lesson_exercises ---
    op.create_table(
        "lesson_exercises",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("lesson_id", sa.BigInteger(), nullable=False),
        sa.Column("order_index", sa.SmallInteger(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("target_sentence", sa.Text(), nullable=False),
        sa.Column("reference_translation", sa.Text(), nullable=False),
        sa.Column("user_translation", sa.Text(), nullable=True),
        sa.Column("target_words", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("suggested_words", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("nontarget_words", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("eval_prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("eval_completion_tokens", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_lesson_exercises"),
        sa.UniqueConstraint("lesson_id", "order_index", name="uq_lesson_exercises_lesson_order"),
        sa.ForeignKeyConstraint(
            ["lesson_id"], ["lessons.id"], ondelete="CASCADE", name="fk_lesson_exercises_lesson_id_lessons"
        ),
        sa.CheckConstraint("order_index > 0", name="ck_lesson_exercises_order_positive"),
        sa.CheckConstraint(
            "status IN ('pending','evaluated')",
            name="ck_lesson_exercises_status_valid",
        ),
        sa.CheckConstraint(
            "char_length(target_sentence) BETWEEN 1 AND 200",
            name="ck_lesson_exercises_target_sentence_length",
        ),
        sa.CheckConstraint(
            "char_length(reference_translation) BETWEEN 1 AND 300",
            name="ck_lesson_exercises_ref_translation_length",
        ),
        sa.CheckConstraint(
            "user_translation IS NULL OR char_length(user_translation) BETWEEN 1 AND 500",
            name="ck_lesson_exercises_user_translation_length",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(target_words) = 'array'",
            name="ck_lesson_exercises_target_words_array",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(suggested_words) = 'array'",
            name="ck_lesson_exercises_suggested_words_array",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(nontarget_words) = 'array'",
            name="ck_lesson_exercises_nontarget_words_array",
        ),
        sa.CheckConstraint(
            "jsonb_array_length(target_words) > 0",
            name="ck_lesson_exercises_target_words_nonempty",
        ),
    )
    op.create_index(
        "ix_lesson_exercises_lesson_order_pending",
        "lesson_exercises",
        ["lesson_id", "order_index"],
        postgresql_where=sa.text("status = 'pending'"),
    )

    # --- prompts ---
    op.create_table(
        "prompts",
        sa.Column("key", sa.String(64), nullable=False),
        sa.Column("system_template", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_by", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("key", name="pk_prompts"),
        sa.ForeignKeyConstraint(
            ["updated_by"], ["users.id"], ondelete="SET NULL", name="fk_prompts_updated_by_users"
        ),
        sa.CheckConstraint(
            "key IN ('generate_sentences','evaluate_translation')",
            name="ck_prompts_key_valid",
        ),
        sa.CheckConstraint(
            "char_length(system_template) BETWEEN 1 AND 8000",
            name="ck_prompts_template_length",
        ),
    )

    # --- llm_calls ---
    op.create_table(
        "llm_calls",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("purpose", sa.String(20), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("lesson_id", sa.BigInteger(), nullable=True),
        sa.Column("exercise_id", sa.BigInteger(), nullable=True),
        sa.Column("attempt", sa.SmallInteger(), nullable=False, server_default=sa.text("1")),
        sa.Column("request", JSONB(), nullable=False),
        sa.Column("response_raw", sa.Text(), nullable=True),
        sa.Column("response_json", JSONB(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("http_status", sa.SmallInteger(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("completion_tokens", sa.Integer(), nullable=True),
        sa.Column("error_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_llm_calls"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL", name="fk_llm_calls_user_id_users"
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"], ["lessons.id"], ondelete="SET NULL", name="fk_llm_calls_lesson_id_lessons"
        ),
        sa.ForeignKeyConstraint(
            ["exercise_id"], ["lesson_exercises.id"], ondelete="SET NULL",
            name="fk_llm_calls_exercise_id_lesson_exercises",
        ),
        sa.CheckConstraint(
            "purpose IN ('generate','evaluate')",
            name="ck_llm_calls_purpose_valid",
        ),
        sa.CheckConstraint(
            "status IN ('ok','http_error','timeout','invalid_json','invalid_schema','validation_failed')",
            name="ck_llm_calls_status_valid",
        ),
        sa.CheckConstraint("attempt >= 1", name="ck_llm_calls_attempt_min"),
    )
    op.create_index("ix_llm_calls_created_at", "llm_calls", ["created_at"])
    op.create_index("ix_llm_calls_user_id", "llm_calls", ["user_id"])
    op.create_index("ix_llm_calls_lesson_id", "llm_calls", ["lesson_id"])
    op.create_index("ix_llm_calls_exercise_id", "llm_calls", ["exercise_id"])

    # --- events ---
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("payload", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_events"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL", name="fk_events_user_id_users"
        ),
        sa.CheckConstraint(
            "char_length(type) BETWEEN 1 AND 64",
            name="ck_events_type_length",
        ),
    )
    op.create_index("ix_events_user_created", "events", ["user_id", "created_at"])
    op.create_index("ix_events_type_created", "events", ["type", "created_at"])


def downgrade() -> None:
    op.drop_table("events")
    op.drop_table("llm_calls")
    op.drop_table("prompts")
    op.drop_table("lesson_exercises")
    op.drop_table("lessons")
    op.drop_table("user_words")
    op.drop_table("words")
    op.drop_table("auth_sessions")
    op.drop_table("users")
