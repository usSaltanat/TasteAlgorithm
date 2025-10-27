from typing import NamedTuple


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
    description: str | None



# class Recipe(NamedTuple):
#     id: int
#     meal: Meal
#     body_meal_recipes: str


class Session(NamedTuple):
    user: User
    session_uuid: str
