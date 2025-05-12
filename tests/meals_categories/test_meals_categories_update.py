import pytest
from storage import MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_meals_category_update_success(client):
    def update_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        assert meals_category.id == 105
        return 105

    def get_meals_category_by_id(id: str) -> MealsCategory | None:
        assert id == 105
        return MealsCategory(105, "ужинучки")

    storage_mock = StorageMock(
        {
            "update_meals_category": update_meals_category,
            "get_meals_category_by_id": get_meals_category_by_id,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals_categories/105/update",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/meals_categories/105"


def test_meals_category_update_failed(client):
    def update_meals_category(meals_category: MealsCategory) -> int | None:
        assert meals_category.name == "ужин"
        assert meals_category.id == 105
        return None

    def get_meals_category_by_id(id: str) -> MealsCategory | None:
        assert id == 105
        return MealsCategory(105, "ужинучки")

    storage_mock = StorageMock(
        {
            "update_meals_category": update_meals_category,
            "get_meals_category_by_id": get_meals_category_by_id,
        }
    )

    app.config["storage"] = storage_mock

    response = client.post(
        "/meals_categories/105/update",
        data={
            "meals_category": "ужин",
        },
    )

    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию блюда</h2>" in html_body
    assert '<label for="meals_category">Новая категория блюда</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert "errorModal" in html_body
    assert "Не удалось изменить категорию блюда" in html_body
