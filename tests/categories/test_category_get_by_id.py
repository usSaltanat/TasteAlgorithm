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


def test_get_category_by_id_empty(client):
    def get_category_by_id_empty(id) -> Category | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_by_id_empty,
        }
    )

    response = client.get("/categories/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "<p>Категория не найдена</p>" in html_body


def test_get_category_by_id_not_empty(client):
    def get_category_by_id_not_empty(id) -> Category | None:
        return Category(1, "Бакалея")

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_by_id_not_empty,
        }
    )

    response = client.get("/categories/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранная категория</h2>" in html_body
    assert '<table id="category_table" class="display">' in html_body
