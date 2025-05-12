import pytest
from storage import Category
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_category_update_success(client):
    def update_category(category: Category) -> int | None:
        assert category.name == "фрукты"
        assert category.id == 105
        return 105

    def get_category_by_id(id: str) -> Category | None:
        assert id == 105
        return Category(105, "фруктыучки")

    storage_mock = StorageMock(
        {
            "update_category": update_category,
            "get_category_by_id": get_category_by_id,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/categories/105/update",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/categories/105"


def test_category_update_failed(client):
    def update_category(category: Category) -> int | None:
        assert category.name == "фрукты"
        assert category.id == 105
        return None

    def get_category_by_id(id: str) -> Category | None:
        assert id == 105
        return Category(105, "фруктыучки")

    storage_mock = StorageMock(
        {
            "update_category": update_category,
            "get_category_by_id": get_category_by_id,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/categories/105/update",
        data={
            "category": "фрукты",
        },
    )

    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию</h2>" in html_body
    assert '<label for="category">Новая категория</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert "errorModal" in html_body
    assert "Не удалось изменить категорию" in html_body
