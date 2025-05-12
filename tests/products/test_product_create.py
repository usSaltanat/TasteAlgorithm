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


def test_product_create_success(client):
    def insert_product(product: Product) -> int | None:
        assert product.name == "Хлеб"
        assert product.category.id == 1
        assert product.unit.id == 2

        return 2025

    storage_mock = StorageMock(
        {
            "insert_product": insert_product,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/products/create",
        data={
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/products/2025"


def test_product_create_failed(client):
    def insert_product(product: Product) -> int | None:
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
            "insert_product": insert_product,
            "get_categories": get_categories,
            "get_units": get_units,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/products/create",
        data={
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)

    assert "<h2>Создать продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body
    assert "errorModal" in html_body
    assert "Не удалось создать продукт" in html_body
