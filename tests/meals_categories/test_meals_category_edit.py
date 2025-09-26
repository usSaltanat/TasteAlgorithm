import pytest
from storage_entities import MealsCategory, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_edit_meals_category_empty(client):
    def get_meals_category_mock_by_id_empty(id: str, user: User) -> MealsCategory | None:
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
            "get_meals_category_by_id": get_meals_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Категория блюда не найдена" in html_body


def test_edit_meals_category_empty_unauthorized(client):
    def get_meals_category_mock_by_id_empty(id: str, user: User) -> MealsCategory | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meals_category_empty_unauthorized_no_cookie_header(client):
    def get_meals_category_mock_by_id_empty(id: str, user: User) -> MealsCategory | None:
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meals_category_not_empty(client):
    def get_meals_category_mock_by_id_not_empty(id: str, user: User) -> MealsCategory | None:
        assert user.id == 1
        assert user.login == "salta"
        return MealsCategory(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию блюда</h2>" in html_body
    assert '<label for="meals_category">Новая категория блюда</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )


def test_edit_meals_category_not_empty_unauthorized(client):
    def get_meals_category_mock_by_id_not_empty(id: str, user: User) -> MealsCategory | None:
        return MealsCategory(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meals_category_not_empty_unauthorized_no_cookie_header(client):
    def get_meals_category_mock_by_id_not_empty(id: str, user: User) -> MealsCategory | None:
        return MealsCategory(1, "Бакалея", user)

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"