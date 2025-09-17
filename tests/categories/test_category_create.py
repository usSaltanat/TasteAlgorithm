import pytest

from main import app
from mocks import StorageMock
from storage import Category, Session, User


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_category_create_success(client):
    def insert_category(category: Category) -> int | None:
        assert category.name == "фрукты"
        return 105

    def find_session_by_uuid(uuid: str) -> Session:
        assert uuid == "5676e01d-1ee1-4339-a6d4-8dfba8f03ecb"
        return Session(
            User(1, "test_login", "test_password_hash"),
            "5676e01d-1ee1-4339-a6d4-8dfba8f03ecb"
        )

    storage_mock = StorageMock(
        {
            "insert_category": insert_category,
            "find_session_by_uuid": find_session_by_uuid,
        }
    )

    app.config["storage"] = storage_mock
    client.set_cookie("session_id", "5676e01d-1ee1-4339-a6d4-8dfba8f03ecb")
    response = client.post(
        "/categories/create",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/categories/105"


def test_category_create_no_auth_cookie(client):
    storage_mock = StorageMock({})

    app.config["storage"] = storage_mock

    response = client.post(
        "/categories/create",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_category_create_unauthorized(client):
    def find_session_by_uuid_failed(uuid: str) -> None:
        assert uuid == "c5f9c844-65c6-4428-b97e-86ced3b0f833"
        return None

    storage_mock = StorageMock({
        "find_session_by_uuid": find_session_by_uuid_failed,
    })

    app.config["storage"] = storage_mock

    client.set_cookie("session_id", "c5f9c844-65c6-4428-b97e-86ced3b0f833")
    response = client.post(
        "/categories/create",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/signin"


def test_category_create_failed(client):
    def find_session_by_uuid(uuid: str) -> Session:
        assert uuid == "6e2a6ea7-5637-43df-a4ac-883fd4a8eeb0"
        return Session(
            User(1, "test_login", "test_password_hash"),
            "6e2a6ea7-5637-43df-a4ac-883fd4a8eeb0"
        )

    def insert_category_failed(category: Category) -> int | None:
        assert category.name == "фрукты"
        return None

    storage_mock = StorageMock(
        {
            "find_session_by_uuid": find_session_by_uuid,
            "insert_category": insert_category_failed,
        }
    )

    app.config["storage"] = storage_mock
    client.set_cookie("session_id", "6e2a6ea7-5637-43df-a4ac-883fd4a8eeb0")
    response = client.post(
        "/categories/create",
        data={
            "category": "фрукты",
        },
    )
    html_body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "<h2>Создать категорию</h2>" in html_body
    assert '<label for="category">Новая категория</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert "errorModal" in html_body
    assert "Не удалось создать категорию" in html_body
