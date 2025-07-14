import pytest
from storage import Category
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_category_create_success(client):
    def insert_category(category: Category) -> int | None:
        assert category.name == "фрукты"
        return 105

    storage_mock = StorageMock(
        {
            "insert_category": insert_category,
        }
    )

    app.config["storage"] = storage_mock
    client.set_cookie("session_id", "test_session")
    response = client.post(
        "/categories/create",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/categories/105"


def test_category_create_failed(client):
    def insert_category(category: Category) -> int | None:
        assert category.name == "фрукты"
        return None

    storage_mock = StorageMock(
        {
            "insert_category": insert_category,
        }
    )

    app.config["storage"] = storage_mock
    client.set_cookie("session_id", "test_session")
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
