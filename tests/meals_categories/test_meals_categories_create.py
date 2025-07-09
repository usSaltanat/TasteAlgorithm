import pytest
from storage import MealsCategory
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

    storage_mock = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals_categories/create",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals_categories/105"


def test_meals_category_create_failed(client):
    def insert_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        return None

    storage_mock = StorageMock(
        {
            "insert_meals_category": insert_meals_category,
        }
    )

    app.config["storage"] = storage_mock

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
