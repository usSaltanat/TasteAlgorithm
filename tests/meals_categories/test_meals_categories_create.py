import pytest
from storage_entities import MealsCategory, User, Session
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_meals_category_create_success(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return 105

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals_categories/105"


def test_meals_category_create_success_unauthorized(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return 105

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meals_category_create_success_unauthorized_no_cookie_header(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return 105

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meals_category_create_failed(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return Session(
            User(1, "salta", "hashqwerty123"),
            session_uuid,
        )

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )
    html_body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "<h2>Создать категорию блюда</h2>" in html_body
    assert '<label for="meals_category">Новая категория блюда</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert "errorModal" in html_body
    assert "Не удалось создать категорию блюда" in html_body


def test_meals_category_create_failed_unauthorized(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        assert session_uuid == "test_session"
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_meals_category_create_failed_unauthorized_no_cookie_header(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return None

    def find_session_by_uuid(session_uuid: str) -> Session | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )
    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"