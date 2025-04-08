from typing import List, NamedTuple, Optional
import pg8000.native
from pg8000.exceptions import DatabaseError
from config_reader import env_config
from contextlib import contextmanager


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


class MealsCategory(NamedTuple):
    id: int
    name: str


class Meal(NamedTuple):
    id: int
    name: str
    meal_category: MealsCategory


class Storage:
    def __init__(self):
        self._connection: Optional[pg8000.native.Connection] = (
            None  # атрибут предназначен для внутреннего использования в классе или модуле.
        )

    def _create_connection(self) -> pg8000.native.Connection:
        if self._connection is None:
            """Создает новое соединение с БД"""
            try:
                self._connection = pg8000.native.Connection(
                    env_config.postgresql_username,
                    database=env_config.postgresql_database,
                    password=env_config.postgresql_password.get_secret_value(),
                    port=env_config.postgresql_port,
                    host=env_config.postgresql_hostname,
                )
                return self._connection
            except DatabaseError as e:
                raise ConnectionError(f"Failed to connect to database: {str(e)}")

    @contextmanager
    def connection(self):
        """Контекстный менеджер для работы с соединением"""
        if self._connection is None:
            self._connection = self._create_connection()

        try:
            yield self._connection
        except DatabaseError as e:
            self._connection = None  # Принудительное переподключение при ошибке
            raise RuntimeError(f"Database operation failed: {str(e)}")

    def close(self):
        """Явное закрытие соединения"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def get_products(self) -> List[ProductView]:
        products_view = []
        with self.connection() as conn:
            for row in conn.run(
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

    def get_product_by_id(self, id: str) -> ProductView | None:
        with self.connection() as conn:
            result = conn.run(
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

    def get_categories(self) -> List[Category]:
        categories = []
        with self.connection() as conn:
            for row in conn.run(
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

    def get_category_by_id(self, id: str) -> Category | None:
        with self.connection() as conn:
            result = conn.run(
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

    def insert_category(self, category: Category) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO categories (category) VALUES (:category) RETURNING id",
                    category=category.name,
                )
                return result[0][0]
        except:
            return None

    def delete_category_by_id(self, id: str) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM categories WHERE id = :category_id RETURNING id",
                    category_id=id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def update_category(self, category: Category) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE categories SET category = :category WHERE id = :id RETURNING id",
                    category=category.name,
                    id=category.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_units(self) -> List[Unit]:
        units = []
        with self.connection() as conn:
            for row in conn.run(
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

    def insert_unit(self, unit: Unit) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO units (unit) VALUES (:unit) RETURNING id",
                    unit=unit.name,
                )
                return result[0][0]
        except:
            return None

    def get_unit_by_id(self, id: str) -> Unit | None:
        with self.connection() as conn:
            result = conn.run(
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

    def delete_unit_by_id(self, id: str) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM units WHERE id = :unit_id RETURNING id", unit_id=id
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def update_unit(self, unit: Unit) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE units SET unit = :unit WHERE id = :id RETURNING id",
                    unit=unit.name,
                    id=unit.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def insert_product(self, product: Product) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO products (unit_id, category_id, product_name) VALUES (:unit_id, :category_id, :product_name) RETURNING id",
                    unit_id=product.unit.id,
                    category_id=product.category.id,
                    product_name=product.name,
                )
                return result[0][0]
        except:
            return None

    def update_product(self, product: Product) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE products SET (unit_id, category_id, product_name) = (:unit_id, :category_id, :product_name) WHERE id = :id RETURNING id",
                    unit_id=product.unit.id,
                    category_id=product.category.id,
                    product_name=product.name,
                    id=product.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def delete_product_by_id(self, id: str) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM products WHERE id = :product_id RETURNING id",
                    product_id=id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_meals_categories(self) -> list[MealsCategory]:
        meals_categories = []
        with self.connection() as conn:
            for row in conn.run(
                """
                    SELECT
                        c.id,
                        c.meals_category
                    FROM meals_categories c
                    ORDER BY c.meals_category
                """
            ):
                meals_categories.append(MealsCategory(row[0], row[1]))
        return meals_categories

    def insert_meals_category(self, meals_category: MealsCategory) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO meals_categories (meals_category) VALUES (:meals_category) RETURNING id",
                    meals_category=meals_category.name,
                )
                return result[0][0]
        except:
            return None

    def get_meals_category_by_id(self, id: str) -> MealsCategory | None:
        with self.connection() as conn:
            result = conn.run(
                """
                    SELECT
                        c.id,
                        c.meals_category
                    FROM meals_categories c
                    WHERE c.id = :meals_category_id
                """,
                meals_category_id=id,
            )
            if len(result) == 0:
                return None
            meals_category = result[0]
            # print("!!!", meals_category)
        return MealsCategory(meals_category[0], meals_category[1])

    def update_meals_category(self, meals_category: MealsCategory) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE meals_categories SET meals_category = :meals_category WHERE id = :id RETURNING id",
                    meals_category=meals_category.name,
                    id=meals_category.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def delete_meals_category_by_id(self, id: str) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM meals_categories WHERE id = :meals_category_id RETURNING id",
                    meals_category_id=id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_meals(self) -> List[Meal]:
        meals_view = []
        with self.connection() as conn:
            for row in conn.run(
                """
                SELECT 
                    m.id,
                    m.meal,
                    mc.meals_category 
                FROM meals m 
                JOIN meals_categories mc ON m.meal_category_id  = mc.id 
                """
            ):
                meals_view.append(Meal(row[0], row[1], row[2]))
        return meals_view

    def get_meal_by_id(self, id: str) -> Meal | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT 
                    m.id,
                    m.meal,
                    mc.meals_category 
                FROM meals m 
                JOIN meals_categories mc ON m.meal_category_id  = mc.id 
                WHERE m.id = :meal_id
                """,
                meal_id=id,
            )
            if len(result) == 0:
                return None
            meal = result[0]
        return Meal(meal[0], meal[1], meal[2])
