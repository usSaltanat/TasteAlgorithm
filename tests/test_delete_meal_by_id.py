import pytest
from typing import List
from storage import Meal
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_meal_by_id_empty(client):
    def delete_meal_by_id_empty(id) -> int | None:
        return None

    def get_meals_mock_empty() -> List[Meal]:
        return []

    app.config["storage"] = StorageMock(
        {
            "delete_meal_by_id": delete_meal_by_id_empty,
            "get_meals": get_meals_mock_empty,
        }
    )

    response = client.get("/meals/1/delete")
    assert response.status_code == 302
    redirect_response = client.get(
        "/meals/1/delete",
        follow_redirects=True,  # Ключевой параметр для следования за редиректом
    )
    assert redirect_response.status_code == 200
    html_body = redirect_response.get_data(as_text=True)
    assert "<h2>Список блюд</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body
    assert "Не удалось удалить блюдо" in html_body


def test_delete_meal_by_id_not_empty(client):
    def delete_meal_by_id_not_empty(id) -> int | None:
        return 1

    def get_meals_mock_empty() -> List[Meal]:
        return []

    app.config["storage"] = StorageMock(
        {
            "delete_meal_by_id": delete_meal_by_id_not_empty,
            "get_meals": get_meals_mock_empty,
        }
    )

    response = client.get("/meals/1/delete")
    assert response.status_code == 302
    redirect_response = client.get(
        "/meals/1/delete",
        follow_redirects=True,  # Ключевой параметр для следования за редиректом
    )
    assert redirect_response.status_code == 200
    html_body = redirect_response.get_data(as_text=True)
    assert "<h2>Список блюд</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body
    assert "Не удалось удалить блюдо" not in html_body
