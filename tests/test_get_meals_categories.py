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


def test_get_meals_categories_empty(client):
    def get_meals_categories_mock_empty() -> List[MealsCategory]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_empty,
        }
    )

    response = client.get("/meals_categories")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список категорий блюд</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_meals_categories_not_empty(client):
    def get_meals_categories_mock_not_empty() -> List[MealsCategory]:
        return [
            MealsCategory(1, "Десерт"),
            MealsCategory(2, "Ужин"),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_not_empty,
        }
    )

    response = client.get("/meals_categories")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список категорий блюд</h2>" in html_body
    assert '<table id="meals_categories_table" class="display">' in html_body
    assert ' $(document).ready(function () {' in html_body   