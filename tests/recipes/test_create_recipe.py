import pytest
from typing import List
from storage import Recipe, Meal, MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_recipe_create_success(client):
    def insert_recipe(recipe: Recipe) -> int | None:
        assert recipe.meal.id == 1
        assert recipe.body_meal_recipes == "aaa"
        return 2025

    storage_mock = StorageMock(
        {
            "insert_recipe": insert_recipe,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/recipes/create",
        data={
            "meal": 1,
            "recipe_body": "aaa",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/recipes/2025"


def test_recipe_create_failed(client):
    def insert_recipe(recipe: Recipe) -> int | None:
        assert recipe.meal.id == 1
        assert recipe.body_meal_recipes == "aaa"
        return None

    def get_recipes_mock_not_empty() -> List[Recipe]:
        return [
            Recipe(
                1,
                Meal(2, "сырники", MealsCategory(3, "десерт")),
                "фффф",
            ),
            Recipe(
                2,
                Meal(3, "бутерброд", MealsCategory(4, "ужин")),
                "бббб",
            ),
        ]

    storage_mock = StorageMock(
        {
            "insert_recipe": insert_recipe,
            "get_recipes": get_recipes_mock_not_empty,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/recipes/create",
        data={
            "meal": 1,
            "recipe_body": "aaa",
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать рецепт</h2>" in html_body
    assert '<div class="recipe_meal_input">' in html_body
    assert '<div class="recipe_body_input">' in html_body
    assert '<option value="2">сырники</option>' in html_body
    assert '<option value="3">бутерброд</option>' in html_body
    assert "errorModal" in html_body
    assert "Не удалось создать рецепт" in html_body
