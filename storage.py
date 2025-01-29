from typing import List, NamedTuple
import pg8000.native

con = pg8000.native.Connection(
    "coderfolder", database="taste_algorithm", password="igor1997"
)


class ProductView(NamedTuple):
    id: int
    name: str
    category: str
    unit: str


class Category(NamedTuple):
    id: int
    name: str | None


class Unit(NamedTuple):
    id: int
    name: str | None


class Product(NamedTuple):
    id: int
    name: str
    category: Category
    unit: Unit


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


def get_product_by_id(id) -> List[ProductView]:
    product_view = []
    query = (
        """ 
            SELECT
                p.id,
                p.product_name,
                c.category,
                u.unit
            FROM products p
            JOIN units u ON p.unit_id = u.id
            JOIN categories c ON p.category_id = c.id
            WHERE p.id = 
            """
        + id
    )
    product = con.run(query)[0]
    product_view.append(ProductView(product[0], product[1], product[2], product[3]))
    return product_view


def get_categories() -> List[Category]:
    categories = []
    for row in con.run(
        """
            SELECT
                c.id,
                c.category
            FROM categories c
            ORDER BY c.category
        """
    ):
        categories.append(Category(row[0], row[1]))
    return categories


def get_units() -> List[Unit]:
    units = []
    for row in con.run(
        """
            SELECT
                u.id,
                u.unit
            FROM units u 
            ORDER BY u.unit
        """
    ):
        units.append(Unit(row[0], row[1]))
    return units


def insert_product(product: Product) -> int:
    [[id]] = con.run(
        "INSERT INTO products (unit_id, category_id, product_name) VALUES (:unit_id, :category_id, :product_name) RETURNING id",
        unit_id=product.unit.id,
        category_id=product.category.id,
        product_name=product.name,
    )
    return id
