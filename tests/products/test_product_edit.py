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


def test_edit_product_empty(client):
    def get_product_mock_by_id_empty(id: str, user: User) -> Product | None:
        assert user.id == 1
        assert user.login == "salta"
        return None

    def get_categories_mock_empty(user: User) -> List[Category]:
        return []

    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_mock_by_id_empty,
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Продукт не найден" in html_body


def test_edit_product_empty_unauthorized(client):
    def get_product_mock_by_id_empty(id: str, user: User) -> Product | None:
        return False

    def get_categories_mock_empty(user: User) -> List[Category]:
        return []

    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_mock_by_id_empty,
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_product_empty_unauthorized_no_cookie_header(client):
    def get_product_mock_by_id_empty(id: str, user: User) -> Product | None:
        return False

    def get_categories_mock_empty(user: User) -> List[Category]:
        return []

    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return False

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_mock_by_id_empty,
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_product_not_empty(client):
    def get_product_mock_by_id_not_empty(id: str, user: User) -> Product | None:
        assert user.id == 1
        assert user.login == "salta"
        return Product(
            1,
            "Молоко",
            Category(1, "Молочные продукты", user),
            Unit(1, "мл", user),
            user,
        )

    def get_categories_mock_not_empty(user: User) -> List[Category]:
        return [Category(1, "бакалея", user), Category(2, "фрукты", user)]

    def get_units_mock_not_empty(user: User) -> List[Unit]:
        return [Unit(1, "шт", user), Unit(2, "гр", user)]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_mock_by_id_not_empty,
            "get_categories": get_categories_mock_not_empty,
            "get_units": get_units_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body
    assert '<option value="1">бакалея</option>' in html_body
    assert '<option value="2">фрукты</option>' in html_body
    assert '<option value="1">шт</option>' in html_body
    assert '<option value="2">гр</option>' in html_body
