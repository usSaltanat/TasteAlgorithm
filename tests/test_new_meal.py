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


def test_new_meal_empty(client):
    def get_meals_categories_mock_empty() -> List[MealsCategory]:
        return []


    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_empty,
        }
    )
    response = client.get("/meals/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body


def test_new_meal_not_empty(client):
    def get_meals_categories_mock_not_empty() -> List[MealsCategory]:
        return [MealsCategory(1, "Десерт"), MealsCategory(2, "Ужин")]

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_not_empty,
        }
    )
    response = client.get("/meals/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert '<option value="1">Десерт</option>' in html_body
    assert '<option value="2">Ужин</option>' in html_body

