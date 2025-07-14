import pytest
from typing import List
from storage import Product, Category, Unit
from main import app
from mocks import StorageMock


# Декоратор @pytest.fixture в сочетании с функцией client()
# создает фикстуру для тестирования Flask-приложений.
# Эта фикстура предоставляет тестовый клиент,
# который имитирует HTTP-запросы к вашему приложению
# без необходимости запуска реального сервера.
@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_products_empty(client):
    def get_products_mock_empty() -> List[Product]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_empty,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список продуктов</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_products_not_empty(client):
    def get_products_mock_not_empty() -> List[Product]:
        return [
            Product(1, "Молоко", Category(1, "Бакалея"), Unit(1, "Литры")),
            Product(2, "Яйца", Category(1, "Бакалея"), Unit(2, "Десятки")),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_not_empty,
        }
    )

    response = client.get("/products")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список продуктов</h2>" in html_body
    assert '<table id="products_table" class="display">' in html_body
    assert " $(document).ready(function () {" in html_body
