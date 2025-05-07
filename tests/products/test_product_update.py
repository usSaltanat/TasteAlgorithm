import pytest
from typing import List
from storage import Category, Unit, Product
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_product_update_success(client):
    def get_product_by_id(id: str) -> Product | None:
        return Product(2025, "Хлебушек", Category(1, "Бакалея"), Unit(2, "шт"))

    def update_product(product: Product) -> int | None:
        assert product.name == "Хлеб"
        assert product.category.id == 1
        assert product.unit.id == 2
        return 2025

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/products/2025/update",
        data={
            "id": 2025,
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/products/2025"


def test_product_update_failed(client):

    def get_product_by_id(id: str) -> Product | None:
        return Product(2025, "Хлебушек", Category(1, "Бакалея"), Unit(2, "шт"))

    def update_product(product: Product) -> int | None:
        return None

    def get_categories() -> List[Category]:
        return [
            Category(1, "Бакалея"),
        ]

    def get_units() -> List[Unit]:
        return [
            Unit(2, "шт"),
        ]

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
            "get_categories": get_categories,
            "get_units": get_units,
        }
    )
    app.config["storage"] = storage_mock

    response = client.get("/products/2025/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body
