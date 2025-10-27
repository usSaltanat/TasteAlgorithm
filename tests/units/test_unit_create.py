import pytest
from storage_entities import Unit, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_unit_create_success(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return 105
    
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/units/105"


def test_unit_create_success_unauthorized(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return 105
    
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_create_success_unauthorized_no_cookie_header(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return 105
    
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_create_failed(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )
    html_body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "<h2>Создать единицу измерения</h2>" in html_body
    assert '<label for="unit">Новая Единица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert 'errorModal' in html_body
    assert 'Не удалось создать единицу измерения' in html_body


def test_unit_create_failed_unauthorized(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return None
    
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_create_failed_unauthorized_no_cookie_header(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return None
    
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_unit": insert_unit,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"