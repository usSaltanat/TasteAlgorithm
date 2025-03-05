from typing import List, NamedTuple
import pg8000.native
from config_reader import env_config

con = pg8000.native.Connection(
    env_config.postgresql_username,
    database=env_config.postgresql_database,
    password=env_config.postgresql_password.get_secret_value(),
    port=env_config.postgresql_port,
    host=env_config.postgresql_hostname,
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


def get_product_by_id(id: str) -> ProductView | None:
    result = con.run(
        """ 
            SELECT
                p.id,
                p.product_name,
                c.category,
                u.unit
            FROM products p
            JOIN units u ON p.unit_id = u.id
            JOIN categories c ON p.category_id = c.id
            WHERE p.id = :product_id
        """,
        product_id=id,
    )
    if len(result) == 0:
        return None
    product = result[0]
    return ProductView(product[0], product[1], product[2], product[3])


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


def get_category_by_id(id: str) -> Category | None:
    result = con.run(
        """
            SELECT
                c.id,
                c.category
            FROM categories c
            WHERE c.id = :category_id
        """,
        category_id=id,
    )
    if len(result) == 0:
        return None
    category = result[0]
    return Category(category[0], category[1])


def insert_category(category: Category) -> int | None:
    try:
        result = con.run(
            "INSERT INTO categories (category) VALUES (:category) RETURNING id",
            category=category.name,
        )
        return result[0][0]
    except:
        return None


def delete_category_by_id(id: str) -> int | None:
    try:
        result = con.run(
            "DELETE FROM categories WHERE id = :category_id RETURNING id",
            category_id=id,
        )
        if len(result) == 0:
            return None
        return result[0][0]
    except:
        return -1


def update_category(category: Category) -> int | None:
    result = con.run(
        "UPDATE categories SET category = :category WHERE id = :id RETURNING id",
        category=category.name,
        id=category.id,
    )
    if len(result) == 0:
        return None
    return result[0][0]


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


def insert_unit(unit: Unit) -> int | None:
    try:
        result = con.run(
            "INSERT INTO units (unit) VALUES (:unit) RETURNING id",
            unit=unit.name,
        )
        return result[0][0]
    except:
        return None


def get_unit_by_id(id: str) -> Unit | None:
    result = con.run(
        """
            SELECT
                u.id,
                u.unit
            FROM units u
            WHERE u.id = :unit_id
        """,
        unit_id=id,
    )
    if len(result) == 0:
        return None
    unit = result[0]
    return Unit(unit[0], unit[1])


def delete_unit_by_id(id: str) -> int | None:
    try:
        result = con.run(
            "DELETE FROM units WHERE id = :unit_id RETURNING id", unit_id=id
        )
        if len(result) == 0:
            return None
        return result[0][0]
    except:
        return -1


def update_unit(unit: Unit) -> int | None:
    result = con.run(
        "UPDATE units SET unit = :unit WHERE id = :id RETURNING id",
        unit=unit.name,
        id=unit.id,
    )
    if len(result) == 0:
        return None
    return result[0][0]


def insert_product(product: Product) -> int | None:
    try:
        result = con.run(
            "INSERT INTO products (unit_id, category_id, product_name) VALUES (:unit_id, :category_id, :product_name) RETURNING id",
            unit_id=product.unit.id,
            category_id=product.category.id,
            product_name=product.name,
        )
        return result[0][0]
    except:
        return None


def update_product(product: Product) -> int | None:
    result = con.run(
        "UPDATE products SET (unit_id, category_id, product_name) = (:unit_id, :category_id, :product_name) WHERE id = :id RETURNING id",
        unit_id=product.unit.id,
        category_id=product.category.id,
        product_name=product.name,
        id=product.id,
    )

    if len(result) == 0:
        return None
    return result[0][0]


def delete_product_by_id(id: str) -> int | None:
    result = con.run(
        "DELETE FROM products WHERE id = :product_id RETURNING id", product_id=id
    )
    if len(result) == 0:
        return None
    return result[0][0]
