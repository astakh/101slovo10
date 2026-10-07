# 101slovo

Веб-приложение для интервального повторения английских слов в контексте предложений.

## Стек

- **Backend:** FastAPI, SQLAlchemy 2.0 async, asyncpg, Alembic, pydantic-settings, Jinja2
- **Frontend:** Jinja2 + HTMX + Alpine.js + Water.css
- **База данных:** PostgreSQL
- **Миграции:** Alembic

## Установка

```bash
# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установить зависимости
pip install -r requirements.txt

# Скопировать .env и заполнить
cp .env.example .env
# Отредактировать .env: DATABASE_URL и SESSION_SECRET
```

## Миграции

```bash
# Применить все миграции
alembic upgrade head

# Откатить все миграции
alembic downgrade base

# Создать новую миграцию
alembic revision --autogenerate -m "description"
```

## Запуск

```bash
uvicorn app.main:app --reload
```

## Проверка

- Health-check: http://127.0.0.1:8000/health
- Главная страница: http://127.0.0.1:8000/
