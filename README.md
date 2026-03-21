# AI Support Analyzer

REST API сервіс для автоматичного аналізу звернень служби підтримки за допомогою штучного інтелекту. Приймає текст від клієнта, класифікує його (категорія, пріоритет) і генерує готову відповідь.

## Стек технологій

- **FastAPI** — асинхронний веб-фреймворк
- **SQLAlchemy 2.0** (async) + **asyncpg** — робота з базою даних
- **PostgreSQL** — зберігання тікетів
- **OpenAI API** — аналіз тексту та генерація відповідей
- **Pydantic v2** — валідація даних
- **Alembic** — міграції бази даних
- **Docker / Docker Compose** — контейнеризація

## Як запустити

### 1. Клонуй репозиторій

```bash
git clone https://github.com/LordClaus/AISupportAnalyzer.git
cd AISupportAnalyzer
```

### 2. Створи файл `.env`

```bash
cp .env.example .env
```

Заповни `.env` своїми значеннями (дивись `.env.example`).

### 3. Запусти через Docker Compose

```bash
docker-compose up --build
```

Сервіс буде доступний на `http://localhost:8000`.

### Запуск без Docker (для розробки)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> Потрібен запущений PostgreSQL та заповнений `.env`.

## API

### `GET /`
Перевірка стану сервісу.

**Відповідь:**
```json
{"message": "База даних підключена, ШІ готовий!"}
```

### `POST /analyze`
Аналізує текст звернення клієнта.

**Тіло запиту:**
```json
{
  "text": "В мене не працює кнопка оплати вже другий день"
}
```

**Відповідь:**
```json
{
  "id": 1,
  "customer_text": "В мене не працює кнопка оплати вже другий день",
  "category": "bug",
  "priority": "high",
  "suggested_response": "Вибачте за незручності! Ми вже розслідуємо проблему з кнопкою оплати і виправимо її найближчим часом.",
  "status": "open"
}
```

**Поля відповіді:**
| Поле | Тип | Опис |
|---|---|---|
| `category` | `bug` / `question` / `feature_request` | Категорія звернення |
| `priority` | `low` / `medium` / `high` | Пріоритет |
| `suggested_response` | string | Готова відповідь клієнту |
| `status` | string | Статус тікета (за замовчуванням `open`) |

## Тести

```bash
pytest tests/
```

## Структура проєкту

```
app/
├── api/
│   └── tickets.py       # Роутери
├── core/
│   └── config.py        # Налаштування через .env
├── db/
│   ├── base.py          # Базовий клас моделей
│   └── session.py       # Підключення до БД
├── models/
│   └── ticket.py        # SQLAlchemy модель тікета
├── schemas/
│   └── ticket.py        # Pydantic схеми
├── services/
│   └── ai_analyzer.py   # Інтеграція з OpenAI
└── main.py              # Точка входу
```