import pytest
from typing import List
from storage import Unit
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_unit_by_id_empty(client):
    def delete_unit_by_id_empty(id) -> int | None:
        assert id == 100500
        return None  # юнит не найден в БД

    app.config["storage"] = StorageMock(
        {
            "delete_unit_by_id": delete_unit_by_id_empty,
        }
    )

    response = client.get("/units/100500/delete")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/units"
    
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get("message")
        assert flash_message == "Не удалось удалить еденицу измерения"


def test_delete_unit_by_id_not_empty(client):
    def delete_unit_by_id_not_empty(id) -> int | None:
        return 1

    app.config["storage"] = StorageMock(
        {
            "delete_unit_by_id": delete_unit_by_id_not_empty,
        }
    )

    response = client.get("/units/1/delete")
    assert response.status_code == 302
