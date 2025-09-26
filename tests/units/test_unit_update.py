import pytest
from storage_entities import Unit, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_unit_update_success(client):
    def update_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        assert unit.id == 105
        return 105

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        assert id == 105
        assert user.id == 1
        assert user.login == "salta"
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/units/105"


def test_unit_update_success_unauthorized(client):
    def update_unit(unit: Unit) -> int | None:
        return 105

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_update_success_unauthorized_no_cookie_header(client):
    def update_unit(unit: Unit) -> int | None:
        return 105

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_update_failed(client):
    def update_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        assert unit.id == 105
        return None

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        assert id == 105
        assert user.id == 1
        assert user.login == "salta"
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить единицу измерения</h2>" in html_body
    assert '<label for="unit">Новая Единица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert "errorModal" in html_body
    assert "Не удалось изменить единицу измерения" in html_body


def test_unit_update_failed_unauthorized(client):
    def update_unit(unit: Unit) -> int | None:
        return None

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    # client.set_cookie("session_id", "test_session")
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_unit_update_failed_unauthorized_no_cookie_header(client):
    def update_unit(unit: Unit) -> int | None:
        return None

    def get_unit_by_id(id: str, user: User) -> Unit | None:
        return Unit(105, "штучки", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/units/105/update",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"
