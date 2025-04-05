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


def test_new_unit(client):
    response = client.get("/units/new")
    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Создать еденицу измерения</h2>" in html_body
    assert '<label for="unit">Новая единица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
