import pytest
from typing import List
from storage_entities import MealsCategory, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_new_meal_empty(client):
    def get_meals_categories_mock_empty(user: User) -> List[MealsCategory]:
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
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body


def test_new_meal_empty_unauthorized(client):
    def get_meals_categories_mock_empty(user: User) -> List[MealsCategory]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_meal_empty_unauthorized_no_cookie_header(client):
    def get_meals_categories_mock_empty(user: User) -> List[MealsCategory]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_meal_not_empty(client):
    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            MealsCategory(1, "Десерт", user),
            MealsCategory(2, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert '<option value="1">Десерт</option>' in html_body
    assert '<option value="2">Ужин</option>' in html_body


def test_new_meal_not_empty_unauthorized(client):
    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Десерт", user),
            MealsCategory(2, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_new_meal_not_empty_unauthorized_no_cookie_header(client):
    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Десерт", user),
            MealsCategory(2, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals/new")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"