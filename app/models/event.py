from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(type) BETWEEN 1 AND 64",
            name="ck_events_type_length",
        ),
        Index("ix_events_user_created", "user_id", "created_at"),
        Index("ix_events_type_created", "type", "created_at"),
    )
