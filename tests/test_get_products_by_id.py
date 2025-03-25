import pytest
from typing import List
from storage import ProductView
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_product_by_id_empty(client):
    def get_product_by_id_empty(id) -> ProductView | None:
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
    def get_product_by_id_not_empty(id) -> ProductView | None:
        return ProductView(1, "Молоко", "Бакалея", "Литры")
    
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