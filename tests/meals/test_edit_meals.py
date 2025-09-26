import pytest
from typing import List
from storage_entities import MealsCategory, Meal, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_edit_meal_empty(client):
    def get_meal_mock_by_id_empty(id: str, user: User) -> Meal | None:
        assert user.id == 1
        assert user.login == "salta"
        return None

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
            "get_meal_by_id": get_meal_mock_by_id_empty,
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Блюдо не найдено" in html_body


def test_edit_meal_empty_unauthorized(client):
    def get_meal_mock_by_id_empty(id: str, user: User) -> Meal | None:
        return None

    def get_meals_categories_mock_empty(user: User) -> List[MealsCategory]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_empty,
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meal_empty_unauthorized_no_cookie_header(client):
    def get_meal_mock_by_id_empty(id: str, user: User) -> Meal | None:
        return None

    def get_meals_categories_mock_empty(user: User) -> List[MealsCategory]:
        return []

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_empty,
            "get_meals_categories": get_meals_categories_mock_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meal_not_empty(client):
    def get_meal_mock_by_id_not_empty(id: str, user: User) -> Meal | None:
        assert user.id == 1
        assert user.login == "salta"
        return Meal(1, "Сырники", MealsCategory(1, "Завтрак", user), user)

    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            MealsCategory(1, "Завтрак", user),
            MealsCategory(2, "Обед", user)
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_not_empty,
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert '<option value="1">Завтрак</option>' in html_body
    assert '<option value="2">Обед</option>' in html_body


def test_edit_meal_not_empty_unauthorized(client):
    def get_meal_mock_by_id_not_empty(id: str, user: User) -> Meal | None:
        return Meal(1, "Сырники", MealsCategory(1, "Завтрак", user), user)

    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Завтрак", user),
            MealsCategory(2, "Обед", user)
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_not_empty,
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.get("/meals/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_edit_meal_not_empty_unauthorized_no_cookie_header(client):
    def get_meal_mock_by_id_not_empty(id: str, user: User) -> Meal | None:
        return Meal(1, "Сырники", MealsCategory(1, "Завтрак", user), user)

    def get_meals_categories_mock_not_empty(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Завтрак", user),
            MealsCategory(2, "Обед", user)
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meal_by_id": get_meal_mock_by_id_not_empty,
            "get_meals_categories": get_meals_categories_mock_not_empty,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.get("/meals/1/edit")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"