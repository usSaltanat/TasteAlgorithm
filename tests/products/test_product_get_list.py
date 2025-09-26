from typing import List

import pytest

from main import app
from mocks import StorageMock
from storage_entities import Product, Category, Unit, User, Session


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
    def get_products_mock_empty(user: User) -> List[Product]:
        assert user.id == 1
        assert user.login == "salta"
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )

    client.set_cookie("session_id", "test_session")
    response = client.get("/products")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список продуктов</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_products_empty_unauthorized(client):
    def get_products_mock_empty(user: User) -> List[Product]:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )

    response = client.get("/products")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_products_empty_unauthorized_no_cookie_header(client):
    def get_products_mock_empty(user: User) -> List[Product]:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert False

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )

    response = client.get("/products")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_products_not_empty(client):
    def get_products_mock_not_empty(user: User) -> List[Product]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            Product(1, "Молоко", Category(1, "Бакалея", user), Unit(1, "Литры", user), user),
            Product(2, "Яйца", Category(1, "Бакалея", user), Unit(2, "Десятки", user), user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_products": get_products_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,            
        }
    )

    client.set_cookie("session_id", "test_session")
    response = client.get("/products")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список продуктов</h2>" in html_body
    assert '<table id="products_table" class="display">' in html_body
    assert " $(document).ready(function () {" in html_body
