import pytest
from typing import List
from storage import MealsCategory
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_meals_category_by_id_empty(client):
    def delete_meals_category_by_id_empty(id) -> int | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_meals_category_by_id": delete_meals_category_by_id_empty,
        }
    )

    response = client.get("/meals_categories/1/delete")
    assert response.status_code == 302


def test_delete_meals_category_by_id_not_empty(client):
    def delete_meals_category_by_id_not_empty(id) -> int | None:
        return 1

    app.config["storage"] = StorageMock(
        {
            "delete_meals_category_by_id": delete_meals_category_by_id_not_empty,
        }
    )

    response = client.get("/meals_categories/1/delete")
    assert response.status_code == 302
