import pytest
from typing import List
from storage import ProductView
from main import app
from mocks import StorageMock
import requests


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as c:
        yield c


def test_delete_product_by_id_empty(client):
    def delete_product_by_id_empty(id) -> int | None:
        return None

    def get_products_mock_empty() -> List[ProductView]:
        return []

    app.config["storage"] = StorageMock(
        {
            "delete_product_by_id": delete_product_by_id_empty,
            "get_products": get_products_mock_empty,
        }
    )

    response = client.get("/products/1/delete")
    assert response.status_code == 302
    redirect_response = client.get(
        "/products/1/delete",
        follow_redirects=True,  # Ключевой параметр для следования за редиректом
    )
    assert redirect_response.status_code == 200
    html_body = redirect_response.get_data(as_text=True)
    assert "<h2>Список продуктов</h2>" in html_body
    assert "<p>Список пуст</p>" in html_body
    assert "Не удалось удалить продукт" in html_body


# def test_delete_product_by_id_not_empty(client):
#     def delete_product_by_id_not_empty(id) -> int | None:
#         return None

#     def get_products_mock_not_empty() -> List[ProductView]:
#         return []

#     app.config["storage"] = StorageMock(
#         {
#             "delete_product_by_id": delete_product_by_id_empty,
#             "get_products": get_products_mock_empty,
#         }
#     )

#     response = client.get("/products/1/delete")
#     assert response.status_code == 302
#     redirect_response = client.get(
#         "/products/1/delete",
#         follow_redirects=True,  # Ключевой параметр для следования за редиректом
#     )
#     assert redirect_response.status_code == 200
#     html_body = redirect_response.get_data(as_text=True)
#     assert "<h2>Список продуктов</h2>" in html_body
#     assert "<p>Список пуст</p>" in html_body
#     assert "Не удалось удалить продукт" in html_body
