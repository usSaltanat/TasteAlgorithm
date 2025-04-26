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


def test_get_unit_by_id_empty(client):
    def get_unit_by_id_empty(id) -> Unit | None:
        return None

    app.config["storage"] = StorageMock(
        {
            "get_unit_by_id": get_unit_by_id_empty,
        }
    )

    response = client.get("/units/1")
    assert response.status_code == 404
    html_body = response.get_data(as_text=True)
    assert "<p>Еденица измерения не найдена</p>" in html_body


def test_get_unit_by_id_not_empty(client):
    def get_unit_by_id_not_empty(id) -> Unit | None:
        return Unit(1, "шт")

    app.config["storage"] = StorageMock(
        {
            "get_unit_by_id": get_unit_by_id_not_empty,
        }
    )

    response = client.get("/units/1")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Выбранная еденица измерения</h2>" in html_body
    assert '<table id="unit_table" class="display">' in html_body
