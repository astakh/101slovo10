from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, Integer, SmallInteger, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    word_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(10), nullable=False, default="active"
    )
    stage: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    due_lesson_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_reviewed_at = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('active','mastered','ignored')",
            name="ck_user_words_status_valid",
        ),
        CheckConstraint("stage BETWEEN 0 AND 6", name="ck_user_words_stage_range"),
        CheckConstraint(
            "due_lesson_number IS NULL OR due_lesson_number > 0",
            name="ck_user_words_due_positive",
        ),
        CheckConstraint(
            "NOT (status = 'active' AND due_lesson_number IS NULL)",
            name="ck_user_words_active_has_due",
        ),
        CheckConstraint(
            "NOT (status <> 'active' AND due_lesson_number IS NOT NULL)",
            name="ck_user_words_inactive_no_due",
        ),
        Index(
            "uq_user_words_user_word",
            "user_id",
            "word_id",
            unique=True,
        ),
        Index(
            "ix_user_words_user_status_due",
            "user_id",
            "status",
            "due_lesson_number",
        ),
        Index(
            "ix_user_words_user_due_active",
            "user_id",
            "due_lesson_number",
            postgresql_where=text("status = 'active'"),
        ),
    )
