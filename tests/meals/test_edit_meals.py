import pytest
from typing import List
from storage import MealsCategory, Meal
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_edit_meal_empty(client):
    def get_meal_mock_by_id_empty(id: str) -> Meal | None:
        return None

    def get_meals_categories_mock_empty() -> List[MealsCategory]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_empty,
            "get_meals_categories": get_meals_categories_mock_empty,
        }
    )
    response = client.get("/meals/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Блюдо не найдено" in html_body


def test_edit_meal_not_empty(client):
    def get_meal_mock_by_id_not_empty(id: str) -> Meal | None:
        return Meal(1, "Сырники", "Завтрак")

    def get_meals_categories_mock_not_empty() -> List[MealsCategory]:
        return [MealsCategory(1, "Завтрак"), MealsCategory(2, "Обед")]

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_not_empty,
            "get_meals_categories": get_meals_categories_mock_not_empty,
        }
    )
    response = client.get("/meals/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert '<option value="1">Завтрак</option>' in html_body
    assert '<option value="2">Обед</option>' in html_body
