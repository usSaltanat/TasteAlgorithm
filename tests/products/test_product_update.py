import pytest
from typing import List
from main import app
from mocks import StorageMock
from storage_entities import Product, Category, Unit, User, Session


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_product_update_success(client):
    def get_product_by_id(id: str, user: User) -> Product | None:
        assert user.id == 1
        assert user.login == "salta"
        return Product(
            2025, "Хлебушек", Category(1, "Бакалея", user), Unit(2, "шт", user), user
        )

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    def update_product(product: Product) -> int | None:
        assert product.name == "Хлеб"
        assert product.category.id == 1
        assert product.unit.id == 2
        assert product.user.id == 1
        return 2025

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )

    app.config["storage"] = storage_mock

    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/products/2025/update",
        data={
            "id": 2025,
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
            "user": 1,            
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/products/2025"


def test_product_update_failed(client):

    def get_product_by_id(id: str, user: User) -> Product | None:
        assert user.id == 1
        assert user.login == "salta"
        return Product(
            2025, "Хлебушек", Category(1, "Бакалея", user), Unit(2, "шт", user), user
        )

    def update_product(product: Product) -> int | None:
        return None

    def get_categories(user: User) -> List[Category]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            Category(1, "Бакалея", user),
        ]

    def get_units(user: User) -> List[Unit]:
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

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
            "get_categories": get_categories,
            "get_units": get_units,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    app.config["storage"] = storage_mock

    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/products/2025/update",
        data={
            "id": 2025,
            "name": "Хлеб",
            "category": 1,
            "unit": 2,
            "user": 1,         
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body
    assert "errorModal" in html_body
    assert "Не удалось изменить продукт" in html_body


def test_product_update_success_unauthorized(client):
    def get_product_by_id(id: str, user: User) -> Product | None:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    def update_product(product: Product, user: User) -> int | None:
        return None

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
            "find_session_by_uuid": find_session_by_uuid,
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
            "user": 1,         
        },
    )
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_product_update_success_unauthorized_no_cookie_header(client):
    def get_product_by_id(id: str, user: User) -> Product | None:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert False

    def update_product(product: Product, user: User) -> int | None:
        return None

    storage_mock = StorageMock(
        {
            "get_product_by_id": get_product_by_id,
            "update_product": update_product,
            "find_session_by_uuid": find_session_by_uuid,
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
            "user": 1,         
        },
    )
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"
