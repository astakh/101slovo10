from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_onboarded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    level: Mapped[str | None] = mapped_column(String(2), nullable=True)
    dictionary_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    words_per_lesson: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    daily_lesson_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    last_lesson_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint("email = lower(email)", name="ck_users_email_lower"),
        CheckConstraint(
            "level IS NULL OR level IN ('A1','A2','B1','B2','C1','C2')",
            name="ck_users_level_valid",
        ),
        CheckConstraint("words_per_lesson >= 1", name="ck_users_words_per_lesson_min"),
        CheckConstraint(
            "daily_lesson_limit >= 1", name="ck_users_daily_lesson_limit_min"
        ),
        CheckConstraint(
            "last_lesson_number >= 0", name="ck_users_last_lesson_number_min"
        ),
        CheckConstraint(
            "NOT is_onboarded OR (timezone IS NOT NULL AND level IS NOT NULL AND dictionary_code IS NOT NULL)",
            name="ck_users_onboarded_fields",
        ),
    )
