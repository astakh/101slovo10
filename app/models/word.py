from sqlalchemy import BigInteger, Boolean, CheckConstraint, Index, String, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    lemma: Mapped[str] = mapped_column(String(64), nullable=False)
    lemma_key: Mapped[str] = mapped_column(String(64), nullable=False)
    pos: Mapped[str] = mapped_column(String(10), nullable=False)
    level: Mapped[str | None] = mapped_column(String(2), nullable=True)
    translations: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False
    )
    in_general: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    in_it: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    in_travel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint(
            "pos IN ('noun','verb','adj','adv','pron','prep','conj','num','det','intj')",
            name="ck_words_pos_valid",
        ),
        CheckConstraint(
            "level IS NULL OR level IN ('A1','A2','B1','B2','C1','C2')",
            name="ck_words_level_valid",
        ),
        CheckConstraint(
            "array_length(translations, 1) BETWEEN 1 AND 5",
            name="ck_words_translations_length",
        ),
        CheckConstraint(
            "char_length(lemma) BETWEEN 1 AND 64",
            name="ck_words_lemma_length",
        ),
        CheckConstraint(
            "char_length(lemma_key) BETWEEN 1 AND 64",
            name="ck_words_lemma_key_length",
        ),
        Index(
            "uq_words_lemma_key_pos",
            "lemma_key",
            "pos",
            unique=True,
        ),
        Index(
            "ix_words_level_general",
            "level",
            postgresql_where=text("in_general = true"),
        ),
        Index(
            "ix_words_level_it",
            "level",
            postgresql_where=text("in_it = true"),
        ),
        Index(
            "ix_words_level_travel",
            "level",
            postgresql_where=text("in_travel = true"),
        ),
    )
