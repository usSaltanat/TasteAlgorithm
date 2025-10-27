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


def test_new_product_empty(client):
    def get_categories_mock_empty(user: User) -> List[Category]:
        assert user.id == 1
        assert user.login == "salta"
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать продукт</h2>" in html_body
    assert '<div class="product_input_label">' in html_body
    assert '<div class="product_category_input">' in html_body
    assert '<div class="product_unit_input">' in html_body


def test_new_product_empty_unauthorized(client):
    def get_categories_mock_empty(user: User) -> List[Category]:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    def get_units_mock_empty(user: User) -> List[Unit]:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_product_empty_unauthorized_no_cookie_header(client):
    def get_categories_mock_empty(user: User) -> List[Category]:
        assert False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert False

    def get_units_mock_empty(user: User) -> List[Unit]:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_categories": get_categories_mock_empty,
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_product_not_empty(client):
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
            "get_categories": get_categories_mock_not_empty,
            "get_units": get_units_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
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
