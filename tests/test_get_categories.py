import pytest
from typing import List
from storage import Category
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_categories_empty(client):
    def get_categories_mock_empty() -> List[Category]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_empty,
        }
    )

    response = client.get("/categories")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список категорий</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_categories_not_empty(client):
    def get_categories_mock_not_empty() -> List[Category]:
        return [
            Category(1, "Бакалея"),
            Category(2, "Фрукты"),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_not_empty,
        }
    )

    response = client.get("/categories")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список категорий</h2>" in html_body
    assert '<table id="categories_table" class="display">' in html_body
