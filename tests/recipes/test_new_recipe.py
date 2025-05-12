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


def test_new_recipe_empty(client):
    def get_recipes_mock_empty() -> List[Recipe]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_recipes": get_recipes_mock_empty,
        }
    )
    response = client.get("/recipes/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать рецепт</h2>" in html_body
    assert '<div class="recipe_meal_input">' in html_body
    assert '<div class="recipe_body_input">' in html_body


def test_new_recipe_not_empty(client):
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

    app.config["storage"] = StorageMock(
        {
            "get_recipes": get_recipes_mock_not_empty,
        }
    )
    response = client.get("/recipes/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать рецепт</h2>" in html_body
    assert '<div class="recipe_meal_input">' in html_body
    assert '<div class="recipe_body_input">' in html_body
    assert '<option value="2">сырники</option>' in html_body
    assert '<option value="3">бутерброд</option>' in html_body
