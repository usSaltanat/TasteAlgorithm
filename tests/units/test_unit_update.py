import pytest
from storage import Unit
from main import app
from mocks import StorageMock


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c

def test_unit_update_success(client):
    def update_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        assert unit.id == 105
        return 105 
    
    def get_unit_by_id(id: str) -> Unit | None:
        assert id == 105
        return Unit(105, "штучки")

    storage_mock = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
        }
    )    

    app.config["storage"] = storage_mock

    response = client.post(
        "/units/105/update",
        data={

            "unit": "шт",
        },
    )

    assert response.status_code == 302
    assert response.headers.get("Location") == "/units/105"


def test_unit_update_failed(client):
    def update_unit(unit: Unit) -> int | None:
        assert unit.name == "шт"
        assert unit.id == 105
        return None
    
    def get_unit_by_id(id: str) -> Unit | None:
        assert id == 105
        return Unit(105, "штучки")

    storage_mock = StorageMock(
        {
            "update_unit": update_unit,
            "get_unit_by_id": get_unit_by_id,
        }
    )    

    app.config["storage"] = storage_mock

    response = client.post(
        "/units/105/update",
        data={

            "unit": "шт",
        },
    )

    assert response.status_code == 200
    html_body = response.get_data(as_text=True)
    assert "<h2>Изменить еденицу измерения</h2>" in html_body
    assert '<label for="unit">Новая еденица измерения</label>' in html_body
    assert (
        '<input class="btn" id="submit" name="submit" type="submit" value="Сохранить">'
        in html_body
    )
    assert 'errorModal' in html_body
    assert 'Не удалось изменить еденицу измерения' in html_body
    

