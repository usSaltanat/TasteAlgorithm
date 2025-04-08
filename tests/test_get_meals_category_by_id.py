import pytest
from typing import List
from storage import MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_meals_category_by_id_empty(client):
    def get_meals_category_by_id_empty(id) -> MealsCategory | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_by_id_empty,
        }
    )

    response = client.get("/meals_categories/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "<p>Категория блюда не найдена</p>" in html_body


def test_get_meals_category_by_id_not_empty(client):
    def get_meals_category_by_id_not_empty(id) -> MealsCategory | None:
        return MealsCategory(1, "Десерт")

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_by_id_not_empty,
        }
    )

    response = client.get("/meals_categories/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранная категория блюда</h2>" in html_body
    assert '<table id="meals_category_table" class="display">' in html_body
