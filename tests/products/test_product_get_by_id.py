import pytest
from typing import List
from storage import Product, Category, Unit
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_product_by_id_empty(client):
    def get_product_by_id_empty(id) -> Product | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_empty,
        }
    )

    response = client.get("/products/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Продукт не найден" in html_body


def test_get_product_by_id_not_empty(client):
    def get_product_by_id_not_empty(id) -> Product | None:
        return Product(1, "Молоко", Category(1, "Бакалея"), Unit(1 ,"Литры"))

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_not_empty,
        }
    )

    response = client.get("/products/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранный продукт</h2>" in html_body
    assert '<table id="products_table" class="display">' in html_body
