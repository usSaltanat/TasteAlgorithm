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


def test_edit_unit_empty(client):
    def get_unit_mock_by_id_empty(id: str) -> Unit | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_unit_by_id": get_unit_mock_by_id_empty,
        }
    )

    response = client.get("/units/1/edit")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "Еденица измерения не найдена" in html_body


def test_edit_unit_not_empty(client):
    def get_unit_mock_by_id_not_empty(id: str) -> Unit | None:
        return Unit(1, "гр")

    app.config["storage"] = StorageMock(
        {
            "get_unit_by_id": get_unit_mock_by_id_not_empty,
        }
    )

    response = client.get("/units/1/edit")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить еденицу измерения</h2>" in html_body
    assert '<label for="unit">Новая еденица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
