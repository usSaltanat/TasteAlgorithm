from typing import List, NamedTuple, Optional
import pg8000.native
from pg8000.exceptions import DatabaseError
from config_reader import env_config
from contextlib import contextmanager

class User(NamedTuple):
    id: int
    login: str
    password_hash: str

class Category(NamedTuple):
    id: int
    name: str | None
    user: User | None


class Unit(NamedTuple):
    id: int
    name: str | None
    user: User | None


class Product(NamedTuple):
    id: int
    name: str
    category: Category
    unit: Unit
    user: User | None


class MealsCategory(NamedTuple):
    id: int
    name: str
    user: User | None


class Meal(NamedTuple):
    id: int
    name: str
    meal_category: MealsCategory
    user: User | None


# class Recipe(NamedTuple):
#     id: int
#     meal: Meal
#     body_meal_recipes: str


class Session(NamedTuple):
    user: User
    session_uuid: str


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
            except DatabaseError as e:
                raise ConnectionError(f"Failed to connect to database: {str(e)}")

        return self._connection

    @contextmanager
    def connection(self):
        """Контекстный менеджер для работы с соединением"""
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

    def find_user_by_login(self, login: str) -> Optional[User]:
        with self.connection() as conn:
            user_rows = conn.run("""
                SELECT
                    u.id as user_id,
                    u.login as user_login,
                    u.password_hash as user_password_hash
                FROM users u
                WHERE u.login = :login
            """, login=login)
        if len(user_rows) == 0:
            return None
        user_row = user_rows[0]
        # print(f"❗️user_row = {user_row}")
        return User(user_row[0], user_row[1], user_row[2])

    def find_session_by_uuid(self, session_uuid: str) -> Session | None:
        with self.connection() as conn:
            session_rows = conn.run("""
                SELECT
                    s.session_uuid,
                    u.id as user_id,
                    u.login as user_login,
                    u.password_hash as user_password_hash
                FROM auth_session s
                JOIN users u ON u.id = s.user_id
                WHERE s.session_uuid = :session_uuid
            """, session_uuid=session_uuid,
            )
        if len(session_rows) == 0:
            return None
        session_row = session_rows[0]
        return Session(
            User(session_row[1], session_row[2], session_row[3]),
            session_row[0],
        )

    def create_session(self, user: User, session_uuid: str) -> None:
        with self.connection() as conn:
            conn.run(
                "INSERT INTO auth_session (user_id, session_uuid) VALUES (:user_id, :session_uuid)",
                user_id=user.id, session_uuid=session_uuid,
            )

    def get_products(self, user: User) -> List[Product]:
        products = []
        with self.connection() as conn:
            for row in conn.run(
                    """
                    SELECT p.id,
                           p.product_name,
                           c.id,
                           c.category,
                           u.id,
                           u.unit
                    FROM products p
                             JOIN units u ON p.unit_id = u.id
                             JOIN categories c ON p.category_id = c.id
                    WHERE p.user_id = :user_id         
                    """,
                    user_id=user.id
            ):
                products.append(
                    Product(
                        int(row[0]),
                        row[1],
                        Category(int(row[2]), row[3], None),
                        Unit(int(row[4]), row[5], None),
                        None
                    )
                )
                # products_view.append(ProductView(row[0], row[1], row[2], row[3]))
        return products

    def get_product_by_id(self, id: str, user: User) -> Product | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT p.id,
                       p.product_name,
                       p.category_id,
                       c.category,
                       p.unit_id,
                       u.unit
                FROM products p
                         JOIN units u ON p.unit_id = u.id
                         JOIN categories c ON p.category_id = c.id
                WHERE p.id = :product_id and p.user_id = :user_id 
                """,
                product_id=id,
                user_id=user.id
            )
            if len(result) == 0:
                return None
            product = result[0]
        return Product(
            int(product[0]),
            product[1],
            Category(int(product[2]), product[3], None),
            Unit(int(product[4]), product[5], None),
            None
        )

    def get_categories(self, user: User) -> List[Category]:
        categories = []
        with self.connection() as conn:
            for row in conn.run(
                    """
                    SELECT c.id,
                           c.category
                    FROM categories c
                    WHERE c.user_id = :user_id 
                    ORDER BY c.category
                    """,
                    user_id=user.id,
            ):
                categories.append(Category(int(row[0]), row[1], None))
        return categories

    def get_category_by_id(self, id: str, user: User) -> Category | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT c.id,
                       c.category
                FROM categories c
                WHERE c.id = :category_id 
                    and c.user_id = :user_id  
                """,
                category_id=id,
                user_id=user.id,
            )
            if len(result) == 0:
                return None
            category = result[0]
        return Category(int(category[0]), category[1], None)

    def insert_category(self, category: Category) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO categories (category, user_id) VALUES (:category, :user_id) RETURNING id",
                    category=category.name,
                    user_id=category.user.id,
                )
                return result[0][0]
        except Exception as e:
            print(e)
            return None

    def delete_category_by_id(self, id: str, user: User) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM categories WHERE id = :category_id and user_id = :user_id RETURNING id",
                    category_id=id,
                    user_id=user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def update_category(self, category: Category, user: User) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE categories SET category = :category WHERE id = :id and user_id = :user_id RETURNING id and user_id = :user_id",
                    category=category.name,
                    id=category.id,
                    user_id=user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_units(self, user: User) -> List[Unit]:
        units = []
        with self.connection() as conn:
            for row in conn.run(
                    """
                    SELECT u.id,
                           u.unit
                    FROM units u
                    WHERE u.user_id = :user_id 
                    ORDER BY u.unit
                    """,
                    user_id=user.id,
            ):
                units.append(Unit(row[0], row[1], None))
        return units

    def insert_unit(self, unit: Unit) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO units (unit, user_id) VALUES (:unit, :user_id) RETURNING id",
                    unit=unit.name,
                    user_id=unit.user.id,
                )
                return result[0][0]
        except:
            return None

    def get_unit_by_id(self, id: str, user: User) -> Unit | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT u.id,
                       u.unit
                FROM units u
                WHERE u.id = :unit_id 
                and u.user_id = :user_id
                """,
                unit_id=id,
                user_id=user.id,
            )
            if len(result) == 0:
                return None
            unit = result[0]
        return Unit(int(unit[0]), unit[1], None)

    def delete_unit_by_id(self, id: str, user: User) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM units WHERE id = :unit_id and user_id = :user_id RETURNING id", 
                    unit_id=id,
                    user_id=user.id,
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
                    "UPDATE units SET unit = :unit WHERE id = :id and user_id = :user_id RETURNING id",
                    unit=unit.name,
                    id=unit.id,
                    user_id=unit.user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def insert_product(self, product: Product) -> int | None:
        try:
            with self.connection() as conn:
                # print("❗️", product.user.id)
                result = conn.run(
                    "INSERT INTO products (unit_id, category_id, product_name, user_id) VALUES (:unit_id, :category_id, :product_name, :user_id) RETURNING id",
                    unit_id=product.unit.id,
                    category_id=product.category.id,
                    product_name=product.name,
                    user_id=product.user.id,

                )
                return result[0][0]
        except:
            return None

    def update_product(self, product: Product) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE products SET (unit_id, category_id, product_name, user_id) = (:unit_id, :category_id, :product_name, :user_id) WHERE id = :id RETURNING id",
                    unit_id=product.unit.id,
                    category_id=product.category.id,
                    product_name=product.name,
                    id=product.id,
                    user_id=product.user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def delete_product_by_id(self, id: str, user: User) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM products WHERE id = :product_id RETURNING id",
                    product_id=id,
                    user_id=user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_meals_categories(self, user: User) -> list[MealsCategory]:
        meals_categories = []
        with self.connection() as conn:
            for row in conn.run(
                    """
                    SELECT c.id,
                           c.meals_category
                    FROM meals_categories c
                    WHERE c.user_id = :user_id
                    ORDER BY c.meals_category
                    """,
                    user_id=user.id,

            ):
                meals_categories.append(MealsCategory(int(row[0]), row[1], None))
        return meals_categories

    def insert_meals_category(self, meals_category: MealsCategory) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO meals_categories (meals_category, user_id) VALUES (:meals_category, :user_id) RETURNING id",
                    meals_category=meals_category.name,
                    user_id=meals_category.user.id,
                )
                return result[0][0]
        except:
            return None

    def get_meals_category_by_id(self, id: str, user: User ) -> MealsCategory | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT c.id,
                       c.meals_category
                FROM meals_categories c
                WHERE c.id = :meals_category_id
                and c.user_id = :user_id
                """,
                meals_category_id=id,
                user_id=user.id,
            )
            if len(result) == 0:
                return None
            meals_category = result[0]
        return MealsCategory(int(meals_category[0]), meals_category[1], None)

    def update_meals_category(self, meals_category: MealsCategory) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE meals_categories SET meals_category = :meals_category WHERE id = :id and user_id = :user_id RETURNING id",
                    meals_category=meals_category.name,
                    id=meals_category.id,
                    user_id=meals_category.user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def delete_meals_category_by_id(self, id: str, user: User) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM meals_categories WHERE id = :meals_category_id and user_id = :user_id RETURNING id",
                    meals_category_id=id,
                    user_id=user.id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def get_meals(self, user: User) -> List[Meal]:
        meals_view = []
        with self.connection() as conn:
            for row in conn.run(
                    """
                    SELECT m.id,
                           m.meal,
                           mc.meals_category
                    FROM meals m
                             JOIN meals_categories mc ON m.meal_category_id = mc.id
                    WHERE m.user_id = :user_id         
                    """,
                    user_id=user.id,
            ):
                meals_view.append(Meal(int(row[0]), row[1], row[2], None))
        return meals_view

    def get_meal_by_id(self, id: str, user: User) -> Meal | None:
        with self.connection() as conn:
            result = conn.run(
                """
                SELECT m.id,
                       m.meal,
                       mc.meals_category
                FROM meals m
                         JOIN meals_categories mc ON m.meal_category_id = mc.id
                WHERE m.id = :meal_id
                      and m.user_id = :user_id
                """,
                meal_id=id,
                user_id=user.id,
            )
            if len(result) == 0:
                return None
            meal = result[0]
        return Meal(int(meal[0]), meal[1], meal[2], None)

    def insert_meal(self, meal: Meal) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "INSERT INTO meals (meal, meal_category_id, user_id) VALUES (:meal, :meal_category_id, :user_id) RETURNING id",
                    meal=meal.name,
                    meal_category_id=meal.meal_category.id,
                    user_id=meal.user.id
                )
                return result[0][0]
        except:
            return None

    def delete_meal_by_id(self, id: str) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "DELETE FROM meals WHERE id = :meal_id RETURNING id",
                    meal_id=id,
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def update_meal(self, meal: Meal) -> int | None:
        try:
            with self.connection() as conn:
                result = conn.run(
                    "UPDATE meals SET ( meal_category_id, meal, user_id) = (:meal_category_id, :meal, :user_id) WHERE id = :id RETURNING id",
                    meal_category_id=meal.meal_category.id,
                    meal=meal.name,
                    id=meal.id,
                    user_id=meal.user.id
                )
                if len(result) == 0:
                    return None
                return result[0][0]
        except:
            return None

    def signup(self, login: str, password_hash: str) -> int:
        with self.connection() as conn:
            result = conn.run(
                "INSERT INTO users (login, password_hash) VALUES (:login, :password_hash) RETURNING id",
                login=login,
                password_hash=password_hash,
            )
            return result[0][0]
