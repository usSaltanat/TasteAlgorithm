import pytest
from storage import Recipe, Meal, MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_recipe_by_id_empty(client):
    def get_recipe_by_id_empty(id) -> Recipe | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_recipe_by_id": get_recipe_by_id_empty,
        }
    )

    response = client.get("/recipes/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Рецепт не найден" in html_body


def test_get_recipe_by_id_not_empty(client):
    def get_recipe_by_id_not_empty(id) -> Recipe | None:
        return Recipe(
            1,
            Meal(2, "сырники", MealsCategory(3, "десерт")),
            "фффф",
        )

    app.config["storage"] = StorageMock(
        {
            "get_recipe_by_id": get_recipe_by_id_not_empty,
        }
    )

    response = client.get("/recipes/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранный рецепт</h2>" in html_body
    assert '<table id="recipes_table" class="display">' in html_body
    assert "сырники" in html_body
    assert "десерт" in html_body
    assert "фффф" in html_body
