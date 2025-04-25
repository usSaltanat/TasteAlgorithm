import pytest
from typing import List
from storage import Meal
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_meals_empty(client):
    def get_meals_mock_empty() -> List[Meal]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_meals": get_meals_mock_empty,
        }
    )

    response = client.get("/meals")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список блюд</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_meals_not_empty(client):
    def get_meals_mock_not_empty() -> List[Meal]:
        return [
            Meal(1, "Сырники", "Десерт"),
            Meal(2, "Бутерброд", "Перекус"),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_meals": get_meals_mock_not_empty,
        }
    )

    response = client.get("/meals")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список блюд</h2>" in html_body
    assert '<table id="meals_table" class="display">' in html_body
    assert ' $(document).ready(function () {' in html_body   