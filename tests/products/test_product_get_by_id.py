import pytest
from storage_entities import Product, Category, Unit, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_product_by_id_empty(client):
    def get_product_by_id_empty(id, user: User) -> Product | None:
        assert user.id == 1
        assert user.login == "salta"
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Продукт не найден" in html_body


def test_get_product_by_id_empty_unauthorized(client):
    def get_product_by_id_empty(id, user: User) -> Product | None:
        return False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_product_by_id_empty_unauthorized_no_cookie_header(client):
    def get_product_by_id_empty(id, user: User) -> Product | None:
        return False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return False

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_product_by_id_not_empty(client):
    def get_product_by_id_not_empty(id, user: User) -> Product | None:
        return Product(
            1, "Молоко", Category(1, "Бакалея", user), Unit(1, "Литры", user), user
        )

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_product_by_id": get_product_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранный продукт</h2>" in html_body
    assert '<table id="products_table" class="display">' in html_body
