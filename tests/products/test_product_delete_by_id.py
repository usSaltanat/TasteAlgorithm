import pytest
from typing import List
from main import app
from mocks import StorageMock
from storage_entities import User, Session


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_product_by_id_empty(client):
    def delete_product_by_id_empty(id, user: User) -> int | None:
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
            "delete_product_by_id": delete_product_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1/delete")
    assert response.status_code == 302
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get("message")
        assert flash_message == "Не удалось удалить продукт"


def test_delete_product_by_id_not_empty(client):
    def delete_product_by_id_not_empty(id, user: User) -> int | None:
        assert user.id == 1
        assert user.login == "salta"
        return 1

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "delete_product_by_id": delete_product_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/products/1/delete")
    assert response.status_code == 302

def test_delete_product_by_id_not_empty_unauthorized(client):
    def delete_product_by_id_not_empty(id, user: User) -> int | None:
        return False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "delete_product_by_id": delete_product_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1/delete")
    assert response.status_code == 302

def test_delete_product_by_id_not_empty_unauthorized_no_cookie_header(client):
    def delete_product_by_id_not_empty(id, user: User) -> int | None:
        return False

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return False

    app.config["storage"] = StorageMock(
        {
            "delete_product_by_id": delete_product_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/products/1/delete")
    assert response.status_code == 302    