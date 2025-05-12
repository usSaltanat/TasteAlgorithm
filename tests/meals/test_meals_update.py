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


def test_meal_update_success(client):
    def get_meal_by_id(id: str) -> Meal | None:
        return Meal(2025, "Сырники", MealsCategory(1, "Завтрак"))

    def update_meal(meal: Meal) -> int | None:
        assert meal.name == "Сырники"
        assert meal.meal_category.id == 1
        return 2025

    storage_mock = StorageMock(
        {
            "get_meal_by_id": get_meal_by_id,
            "update_meal": update_meal,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals/2025/update",
        data={
            "id": 2025,
            "name": "Сырники",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals/2025"


def test_meal_update_failed(client):

    def get_meal_by_id(id: str) -> Meal | None:
        return Meal(2025, "Сырники", MealsCategory(1, "Десерт"))

    def update_meal(meal: Meal) -> int | None:
        return None

    def get_meals_categories() -> List[MealsCategory]:
        return [
            MealsCategory(1, "Десерт"),
        ]

    storage_mock = StorageMock(
        {
            "get_meal_by_id": get_meal_by_id,
            "update_meal": update_meal,
            "get_meals_categories": get_meals_categories,
        }
    )
    app.config["storage"] = storage_mock

    response = client.post(
        "/meals/2025/update",
        data={
            "id": 2025,
            "name": "Сырники",
            "meals_category": 1,
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert "errorModal" in html_body
    assert "Не удалось изменить блюдо" in html_body
