import pytest
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_recipe_by_id_empty(client):
    def delete_recipe_by_id_empty(id) -> int | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "delete_recipe_by_id": delete_recipe_by_id_empty,
        }
    )

    response = client.get("/recipes/1/delete")
    assert response.status_code == 302
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get("message")
        assert flash_message == "Не удалось удалить рецепт"


def test_delete_recipe_by_id_not_empty(client):
    def delete_recipe_by_id_not_empty(id) -> int | None:
        return 1

    app.config["storage"] = StorageMock(
        {
            "delete_recipe_by_id": delete_recipe_by_id_not_empty,
        }
    )

    response = client.get("/recipes/1/delete")
    assert response.status_code == 302
