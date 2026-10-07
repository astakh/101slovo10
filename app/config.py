from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/101slovo"
    SESSION_SECRET: str = "change-me-to-a-long-random-string"
    SESSION_COOKIE_NAME: str = "101slovo_session"
    SESSION_TTL_DAYS: int = 30
    WORDS_PER_LESSON_DEFAULT: int = 5
    WORDS_PER_LESSON_MIN: int = 1
    WORDS_PER_LESSON_MAX: int = 10
    DAILY_LESSON_LIMIT_DEFAULT: int = 1
    DAILY_LESSON_LIMIT_MAX: int = 5
    GIGACHAT_AUTH_KEY: str = ""
    GIGACHAT_SCOPE: str = "GIGACHAT_API_PERS"
    GIGACHAT_MODEL: str = "GigaChat"
    GIGACHAT_VERIFY_SSL: bool = False
    GEN_TEMPERATURE: float = 0.7
    EVAL_TEMPERATURE: float = 0.2
    LLM_LOG_RETENTION_DAYS: int = 90

    def model_post_init(self, __context: object) -> None:
        url = self.DATABASE_URL
        if url.startswith("postgresql+asyncpg://"):
            pass
        elif url.startswith("postgresql://"):
            self.DATABASE_URL = url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )
        elif url.startswith("postgres://"):
            self.DATABASE_URL = url.replace(
                "postgres://", "postgresql+asyncpg://", 1
            )


settings = Settings()
