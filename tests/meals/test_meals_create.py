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


def test_meal_create_success(client):
    def insert_meal(meal: Meal) -> int | None:
        assert meal.name == "Борщ"
        assert meal.meal_category.id == 1
        return 2025

    storage_mock = StorageMock(
        {
            "insert_meal": insert_meal,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals/2025"


def test_meal_create_failed(client):
    def insert_meal(meal: Meal) -> int | None:
        assert meal.name == "Борщ"
        assert meal.meal_category.id == 1
        return None

    def get_meals_categories() -> List[MealsCategory]:
        return [
            MealsCategory(1, "Ужин"),
        ]

    storage_mock = StorageMock(
        {
            "insert_meal": insert_meal,
            "get_meals_categories": get_meals_categories,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert "errorModal" in html_body
    assert "Не удалось создать блюдо" in html_body
