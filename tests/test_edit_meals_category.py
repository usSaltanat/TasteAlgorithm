import pytest
from storage import MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_edit_meals_category_empty(client):
    def get_meals_category_mock_by_id_empty(id: str) -> MealsCategory | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_empty,
        }
    )

    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Категория блюда не найдена" in html_body


def test_edit_meals_category_not_empty(client):
    def get_meals_category_mock_by_id_not_empty(id: str) -> MealsCategory | None:
        return MealsCategory(1, "Бакалея")

    app.config["storage"] = StorageMock(
        {
            "get_meals_category_by_id": get_meals_category_mock_by_id_not_empty,
        }
    )

    response = client.get("/meals_categories/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить категорию блюда</h2>" in html_body
    assert '<label for="meals_category">Новая категория блюда</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
