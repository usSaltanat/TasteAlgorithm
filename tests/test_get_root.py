import pytest
from storage_entities import User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_root_success(client):
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/products"


def test_get_root_unauthorized(client):
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_root_unauthorized_no_cookie_header(client):
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"