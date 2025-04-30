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
    # по хорошему ещё проверить текст flash сообщения
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get("message")
        assert flash_message == "Не удалось удалить еденицу измерения"


def test_delete_unit_by_id_not_empty(client):
    def delete_unit_by_id_not_empty(id) -> int | None:
        return 1

    def get_units_mock_empty() -> List[Unit]:
        return []

    app.config["storage"] = StorageMock(
        {
            "delete_unit_by_id": delete_unit_by_id_not_empty,
            "get_units": get_units_mock_empty,
        }
    )

    response = client.get("/units/1/delete")
    assert response.status_code == 302
    redirect_response = client.get(
        "/units/1/delete",
        follow_redirects=True,  # Ключевой параметр для следования за редиректом
    )
    assert redirect_response.status_code == 200
    html_body = redirect_response.get_data(as_text=True)
    assert "<h2>Список едениц измерения</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body
