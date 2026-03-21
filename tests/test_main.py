from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    mock_engine = MagicMock()
    mock_conn = AsyncMock()
    mock_conn.run_sync = AsyncMock()
    mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)

    with patch("app.main.engine", mock_engine):
        from app.main import app
        with TestClient(app) as c:
            yield c


def test_read_root(client):
    """Тестуємо, чи працює головна сторінка"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "База даних підключена, ШІ готовий!"}


@patch("app.main.analyze_ticket_text", new_callable=AsyncMock)
@patch("app.main.get_db")
def test_create_ticket(mock_get_db, mock_analyze, client):
    """Тестуємо створення тікета з моканням ШІ та БД"""
    mock_analyze.return_value = {
        "category": "bug",
        "priority": "high",
        "suggested_response": "Вибачте за незручності, ми вже працюємо над вирішенням.",
    }

    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()

    from app.models.ticket import Ticket
    fake_ticket = Ticket(
        id=1,
        customer_text="Тестове звернення про помилку",
        category="bug",
        priority="high",
        suggested_response="Вибачте за незручності, ми вже працюємо над вирішенням.",
        status="open",
    )
    mock_db.refresh = AsyncMock(side_effect=lambda obj: obj.__dict__.update(fake_ticket.__dict__))

    async def override_get_db():
        yield mock_db

    mock_get_db.return_value = override_get_db()

    from app.main import app
    from app.db.session import get_db
    app.dependency_overrides[get_db] = override_get_db

    response = client.post("/analyze", json={"text": "Тестове звернення про помилку"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "bug"
    assert data["priority"] == "high"
    assert "id" in data