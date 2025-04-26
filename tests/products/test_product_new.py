import pytest
from typing import List
from storage import Category, Unit
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_new_product_empty(client):
    def get_categories_mock_empty() -> List[Category]:
        return []

    def get_units_mock_empty() -> List[Unit]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
        }
    )
    response = client.get("/products/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body


def test_new_product_not_empty(client):
    def get_categories_mock_not_empty() -> List[Category]:
        return [Category(1, 'бакалея'), Category(2, 'фрукты')]

    def get_units_mock_not_empty() -> List[Unit]:
        return [Unit(1, 'шт'), Unit(2, 'гр')]

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_not_empty,
            "get_units": get_units_mock_not_empty,
        }
    )
    response = client.get("/products/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body
    assert '<option value="1">бакалея</option>' in html_body
    assert '<option value="2">фрукты</option>' in html_body
    assert '<option value="1">шт</option>' in html_body
    assert '<option value="2">гр</option>' in html_body

