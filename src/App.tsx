export default function App() {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <h1>101slovo</h1>
      <p>Веб-приложение для интервального повторения английских слов в контексте предложений.</p>
      
      <h2>Стек</h2>
      <ul>
        <li><strong>Backend:</strong> FastAPI, SQLAlchemy 2.0 async, asyncpg, Alembic, pydantic-settings, Jinja2</li>
        <li><strong>Frontend:</strong> Jinja2 + HTMX + Alpine.js + Water.css</li>
        <li><strong>База данных:</strong> PostgreSQL</li>
        <li><strong>Миграции:</strong> Alembic</li>
      </ul>

      <h2>Установка и запуск</h2>
      <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '4px', overflow: 'auto' }}>
{`# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Скопировать .env и заполнить
cp .env.example .env

# Применить миграции
alembic upgrade head

# Запустить приложение
uvicorn app.main:app --reload`}
      </pre>

      <h2>Проверка</h2>
      <ul>
        <li>Health-check: <code>GET /health</code> → <code>{'{"status":"ok"}'}</code></li>
        <li>Главная страница: <code>GET /</code></li>
      </ul>

      <h2>Структура проекта</h2>
      <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '4px', overflow: 'auto' }}>
{`101slovo/
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   └── models/
│       ├── __init__.py
│       ├── base.py
│       ├── user.py
│       ├── auth_session.py
│       ├── word.py
│       ├── user_word.py
│       ├── lesson.py
│       ├── lesson_exercise.py
│       ├── prompt.py
│       ├── llm_call.py
│       └── event.py
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   └── css/
│       └── custom.css
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        └── 0001_initial.py`}
      </pre>
    </div>
  );
}
