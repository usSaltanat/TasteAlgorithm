from typing import List, NamedTuple
import pg8000.native

con = pg8000.native.Connection("oleg", database="taste_algorithm", password="1988")


class ProductView(NamedTuple):
    id: int
    name: str
    category: str
    unit: str


def get_products() -> List[ProductView]:
    products_view = []
    for row in con.run(
        """
            SELECT
                p.id,
                p.product_name,
                c.category,
                u.unit
            FROM products p
            JOIN units u ON p.unit_id = u.id
            JOIN categories c ON p.category_id = c.id
        """
    ):
        products_view.append(ProductView(row[0], row[1], row[2], row[3]))
    return products_view


def insert_product(product) -> int:
    # TODO
    # id = len(products)
    # products.append(
    #     Product(
    #         id,
    #         product.name,
    #         product.category_id,
    #         product.unit_id,
    #     )
    # )
    # return id
    return -1
