import pytest
from typing import List
from storage import Recipes
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_recipes_empty(client):
    def get_recipes_mock_empty() -> List[Recipes]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_recipes": get_recipes_mock_empty,
        }
    )

    response = client.get("/recipes")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список рецептов</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_recipes_not_empty(client):
    def get_recipes_mock_not_empty() -> List[Recipes]:
        return [
            Recipes(1, "сырники", "десерт", "фффф"),
            Recipes(2, "бутерброд", "ужин", "бббб"),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_recipes": get_recipes_mock_not_empty,
        }
    )

    response = client.get("/recipes")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список рецептов</h2>" in html_body
    assert '<table id="recipes_table" class="display">' in html_body
    assert "<td>сырники</td>" in html_body
    assert "<td>десерт</td>" in html_body
    assert '<td><a href="/recipes/1">фффф</a></td>' in html_body
    assert '<td><a href="/recipes/2">бббб</a></td>' in html_body
    assert " $(document).ready(function () {" in html_body
