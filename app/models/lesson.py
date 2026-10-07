from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_number: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="in_progress"
    )
    started_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    completed_at = mapped_column(DateTime(timezone=True), nullable=True)
    started_local_date = mapped_column(Date, nullable=False)
    completed_local_date = mapped_column(Date, nullable=True)
    gen_prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gen_completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("lesson_number > 0", name="ck_lessons_number_positive"),
        CheckConstraint(
            "char_length(idempotency_key) BETWEEN 1 AND 128",
            name="ck_lessons_idempotency_key_length",
        ),
        CheckConstraint(
            "status IN ('in_progress','completed')",
            name="ck_lessons_status_valid",
        ),
        CheckConstraint(
            "NOT (status = 'completed' AND (completed_at IS NULL OR completed_local_date IS NULL))",
            name="ck_lessons_completed_fields",
        ),
        CheckConstraint(
            "NOT (status = 'in_progress' AND (completed_at IS NOT NULL OR completed_local_date IS NOT NULL))",
            name="ck_lessons_in_progress_fields",
        ),
        Index(
            "uq_lessons_user_number",
            "user_id",
            "lesson_number",
            unique=True,
        ),
        Index(
            "uq_lessons_user_idempotency",
            "user_id",
            "idempotency_key",
            unique=True,
        ),
        Index(
            "ix_lessons_user_started_date",
            "user_id",
            "started_local_date",
        ),
        Index(
            "ix_lessons_user_completed_date",
            "user_id",
            "completed_local_date",
        ),
        Index(
            "uq_lessons_user_in_progress",
            "user_id",
            unique=True,
            postgresql_where=text("status = 'in_progress'"),
        ),
    )
