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


def test_edit_category_empty(client):
    def get_category_mock_by_id_empty(id: str) -> Category | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_empty,
        }
    )

    response = client.get("/categories/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Категория не найдена" in html_body


def test_edit_category_not_empty(client):
    def get_category_mock_by_id_not_empty(id: str) -> Category | None:
        return Category(1, "Бакалея")

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_not_empty,
        }
    )

    response = client.get("/categories/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию</h2>" in html_body
    assert '<label for="category">Новая категория</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
