import pytest
from storage import Meal
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_meal_by_id_empty(client):
    def get_meal_by_id_empty(id) -> Meal | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_by_id_empty,
        }
    )

    response = client.get("/meals/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Блюдо не найдено" in html_body


def test_get_meal_by_id_not_empty(client):
    def get_meal_by_id_not_empty(id) -> Meal | None:
        return Meal(1, "Сырники", "Десерт")

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_by_id_not_empty,
        }
    )

    response = client.get("/meals/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранное блюдо</h2>" in html_body
    assert '<table id="meals_table" class="display">' in html_body
