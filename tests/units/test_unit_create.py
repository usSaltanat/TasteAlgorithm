import pytest
from storage import Unit
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c

def test_unit_create_success(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return 105 
    
    storage_mock = StorageMock(
        {
            "insert_unit": insert_unit,
        }
    )    

    app.config["storage"] = storage_mock

    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/units/105"

def test_unit_create_failed(client):
    def insert_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        return None 

    storage_mock = StorageMock(
        {
            "insert_unit": insert_unit,
        }
    )    

    app.config["storage"] = storage_mock

    response = client.post(
        "/units/create",
        data={
            "unit": "шт",
        },
    )
    html_body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "<h2>Создать еденицу измерения</h2>" in html_body
    assert '<label for="unit">Новая еденица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert 'errorModal' in html_body
    assert 'Не удалось создать еденицу измерения' in html_body



