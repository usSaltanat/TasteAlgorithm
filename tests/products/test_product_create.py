import pytest
from typing import List
from storage_entities import Category, Unit, Product, User, Session
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

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_product": insert_product,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
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


def test_product_create_success_unauthorized(client):
    def insert_product(product: Product) -> int | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_product": insert_product,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/products/create",
        data={
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_product_create_success_unauthorized_no_cookie_header(client):
    def insert_product(product: Product) -> int | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_product": insert_product,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/products/create",
        data={
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_product_create_failed(client):
    def insert_product(product: Product) -> int | None:
        return None

    def get_categories_mock(user: User) -> List[Category]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            Category(1, "Бакалея", user),
        ]

    def get_units_mock(user: User) -> List[Unit]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            Unit(2, "шт", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_product": insert_product,
            "get_categories": get_categories_mock,
            "get_units": get_units_mock,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
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