import pytest
from storage_entities import Category, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_edit_category_empty(client):
    def get_category_mock_by_id_empty(id: str, user: User) -> Category | None:
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
            "get_category_by_id": get_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Категория не найдена" in html_body


def test_edit_category_empty_unauthorized(client):
    def get_category_mock_by_id_empty(id: str, user: User) -> Category | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_category_empty_unauthorized_no_cookie_header(client):
    def get_category_mock_by_id_empty(id: str, user: User) -> Category | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_category_not_empty(client):
    def get_category_mock_by_id_not_empty(id: str, user: User) -> Category | None:
        assert user.id == 1
        assert user.login == "salta"
        return Category(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию</h2>" in html_body
    assert '<label for="category">Новая категория</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )


def test_edit_category_not_empty_unauthorized(client):
    def get_category_mock_by_id_not_empty(id: str, user: User) -> Category | None:
        return Category(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_category_not_empty_unauthorized_no_cookie_header(client):
    def get_category_mock_by_id_not_empty(id: str, user: User) -> Category | None:
        return Category(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_category_by_id": get_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"