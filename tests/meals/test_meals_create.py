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


def test_meal_create_success(client):
    def insert_meal(meal: Meal) -> int | None:
        assert meal.name == "Борщ"
        assert meal.meal_category.id == 1
        return 2025

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals/2025"


def test_meal_create_success_unauthorized(client):
    def insert_meal(meal: Meal) -> int | None:
        return 2025

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meal_create_success_unauthorized_no_cookie_header(client):
    def insert_meal(meal: Meal) -> int | None:
        return 2025

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meal_create_failed(client):
    def insert_meal(meal: Meal) -> int | None:
        assert meal.name == "Борщ"
        assert meal.meal_category.id == 1
        return None

    def get_meals_categories_mock(user: User) -> List[MealsCategory]:
        assert user.id == 1
        assert user.login == "salta"
        return [
            MealsCategory(1, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "get_meals_categories": get_meals_categories_mock,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать блюдо</h2>" in html_body
    assert '<div class="meal_input_label">' in html_body
    assert '<div class="meal_category_input">' in html_body
    assert "errorModal" in html_body
    assert "Не удалось создать блюдо" in html_body


def test_meal_create_failed_unauthorized(client):
    def insert_meal(meal: Meal) -> int | None:
        return None

    def get_meals_categories_mock(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "get_meals_categories": get_meals_categories_mock,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meal_create_failed_unauthorized_no_cookie_header(client):
    def insert_meal(meal: Meal) -> int | None:
        return None

    def get_meals_categories_mock(user: User) -> List[MealsCategory]:
        return [
            MealsCategory(1, "Ужин", user),
        ]

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meal": insert_meal,
            "get_meals_categories": get_meals_categories_mock,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/meals/create",
        data={
            "name": "Борщ",
            "meals_category": 1,
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"