import pytest
from storage_entities import User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_new_meals_category(client):
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
    response = client.get("/meals_categories/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать категорию блюда</h2>" in html_body
    assert '<label for="meals_category">Новая категория блюда</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )


def test_new_meals_category_unauthorized(client):
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals_categories/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_meals_category_unauthorized_no_cookie_header(client):
    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals_categories/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"