import pytest
from typing import List
from storage_entities import Unit, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_units_empty(client):
    def get_units_mock_empty(user: User) -> List[Unit]:
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
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/units")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список единиц измерения</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_units_empty_unauthorized(client):
    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.get("/units")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_units_empty_unauthorized_no_cookie_header(client):
    def get_units_mock_empty(user: User) -> List[Unit]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/units")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_units_not_empty(client):
    def get_units_mock_not_empty(user: User) -> List[Unit]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            Unit(1, "шт", user),
            Unit(2, "л", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/units")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список единиц измерения</h2>" in html_body
    assert '<table id="units_table" class="display">' in html_body
    assert " $(document).ready(function () {" in html_body


def test_get_units_not_empty_unauthorized(client):
    def get_units_mock_not_empty(user: User) -> List[Unit]:
        return [
            Unit(1, "шт", user),
            Unit(2, "л", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.get("/units")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_get_units_not_empty_unauthorized_no_cookie_header(client):
    def get_units_mock_not_empty(user: User) -> List[Unit]:
        return [
            Unit(1, "шт", user),
            Unit(2, "л", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/units")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"