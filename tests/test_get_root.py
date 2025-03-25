import pytest

from main import app


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_get_root_success(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/products"

