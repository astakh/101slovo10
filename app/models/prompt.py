from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Prompt(Base):
    __tablename__ = "prompts"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    system_template: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "key IN ('generate_sentences','evaluate_translation')",
            name="ck_prompts_key_valid",
        ),
        CheckConstraint(
            "char_length(system_template) BETWEEN 1 AND 8000",
            name="ck_prompts_template_length",
        ),
    )
