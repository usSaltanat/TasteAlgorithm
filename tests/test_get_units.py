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


def test_get_units_empty(client):
    def get_units_mock_empty() -> List[Unit]:
        return []

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_empty,
        }
    )

    response = client.get("/units")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список едениц измерения</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body


def test_get_units_not_empty(client):
    def get_units_mock_not_empty() -> List[Unit]:
        return [
            Unit(1, "шт"),
            Unit(2, "л"),
        ]

    app.config["storage"] = StorageMock(
        {
            "get_units": get_units_mock_not_empty,
        }
    )

    response = client.get("/units")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Список едениц измерения</h2>" in html_body
    assert '<table id="units_table" class="display">' in html_body
