import pytest
from storage_entities import User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_category_by_id_empty(client):
    def delete_category_by_id_empty(id, user: User) -> int | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/delete")
    assert response.status_code == 302
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get("message")
        assert flash_message == "Не удалось удалить категорию"


def test_delete_category_by_id_empty_unauthorized(client):
    def delete_category_by_id_empty(id, user: User) -> int | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/delete")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_delete_category_by_id_empty_unauthorized_no_cookie_header(client):
    def delete_category_by_id_empty(id, user: User) -> int | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/categories/1/delete")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_delete_category_by_id_not_empty(client):
    def delete_category_by_id_not_empty(id, user: User) -> int | None:
        return 1

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/delete")
    assert response.status_code == 302


def test_delete_category_by_id_not_empty_unauthorized(client):
    def delete_category_by_id_not_empty(id, user: User) -> int | None:
        return 1

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/delete")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_delete_category_by_id_not_empty_unauthorized_no_cookie_header(client):
    def delete_category_by_id_not_empty(id, user: User) -> int | None:
        return 1

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_category_by_id": delete_category_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/categories/1/delete")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"