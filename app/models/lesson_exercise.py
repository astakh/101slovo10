from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, Integer, SmallInteger, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class LessonExercise(Base):
    __tablename__ = "lesson_exercises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    target_sentence: Mapped[str] = mapped_column(Text, nullable=False)
    reference_translation: Mapped[str] = mapped_column(Text, nullable=False)
    user_translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_words = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    suggested_words = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    nontarget_words = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    eval_prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    eval_completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("order_index > 0", name="ck_lesson_exercises_order_positive"),
        CheckConstraint(
            "status IN ('pending','evaluated')",
            name="ck_lesson_exercises_status_valid",
        ),
        CheckConstraint(
            "char_length(target_sentence) BETWEEN 1 AND 200",
            name="ck_lesson_exercises_target_sentence_length",
        ),
        CheckConstraint(
            "char_length(reference_translation) BETWEEN 1 AND 300",
            name="ck_lesson_exercises_ref_translation_length",
        ),
        CheckConstraint(
            "user_translation IS NULL OR char_length(user_translation) BETWEEN 1 AND 500",
            name="ck_lesson_exercises_user_translation_length",
        ),
        CheckConstraint(
            "jsonb_typeof(target_words) = 'array'",
            name="ck_lesson_exercises_target_words_array",
        ),
        CheckConstraint(
            "jsonb_typeof(suggested_words) = 'array'",
            name="ck_lesson_exercises_suggested_words_array",
        ),
        CheckConstraint(
            "jsonb_typeof(nontarget_words) = 'array'",
            name="ck_lesson_exercises_nontarget_words_array",
        ),
        CheckConstraint(
            "jsonb_array_length(target_words) > 0",
            name="ck_lesson_exercises_target_words_nonempty",
        ),
        Index(
            "uq_lesson_exercises_lesson_order",
            "lesson_id",
            "order_index",
            unique=True,
        ),
        Index(
            "ix_lesson_exercises_lesson_order_pending",
            "lesson_id",
            "order_index",
            postgresql_where=text("status = 'pending'"),
        ),
    )
