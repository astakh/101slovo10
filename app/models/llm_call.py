from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class LLMCall(Base):
    __tablename__ = "llm_calls"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    purpose: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    lesson_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )
    exercise_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("lesson_exercises.id", ondelete="SET NULL"),
        nullable=True,
    )
    attempt: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    request = mapped_column(JSONB, nullable=False)
    response_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_json = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    http_status: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_code: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "purpose IN ('generate','evaluate')",
            name="ck_llm_calls_purpose_valid",
        ),
        CheckConstraint(
            "status IN ('ok','http_error','timeout','invalid_json','invalid_schema','validation_failed')",
            name="ck_llm_calls_status_valid",
        ),
        CheckConstraint("attempt >= 1", name="ck_llm_calls_attempt_min"),
        Index("ix_llm_calls_created_at", "created_at"),
        Index("ix_llm_calls_user_id", "user_id"),
        Index("ix_llm_calls_lesson_id", "lesson_id"),
        Index("ix_llm_calls_exercise_id", "exercise_id"),
    )
