from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app

client = TestClient(app)


def test_read_root():
    """Тестуємо, чи працює головна сторінка"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "База даних підключена, ШІ готовий!"}


@patch("app.main.analyze_ticket_text", new_callable=AsyncMock)
def test_create_ticket(mock_analyze):
    """Тестуємо створення тікета з моканням (імітацією) ШІ"""

    mock_analyze.return_value = {
        "category": "refund",
        "priority": "high",
        "suggested_response": "Тестова відповідь: повернемо кошти."
    }

    test_payload = {"text": "Тестове звернення про повернення"}
    response = client.post("/analyze", json=test_payload)

    assert response.status_code == 200

    data = response.json()
    assert data["customer_text"] == "Тестове звернення про повернення"
    assert data["category"] == "refund"
    assert data["priority"] == "high"

    assert "id" in data