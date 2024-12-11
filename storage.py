from typing import NamedTuple, List


class Product(NamedTuple):
    id: int
    name: str
    category_id: int
    unit_id: int


class Category(NamedTuple):
    id: int
    name: str


class Unit(NamedTuple):
    id: int
    name: str


def get_products() -> List[Product]:
    # тут может быть SQL SELECT...
    return [
        Product(1, "Хлеб", 1, 1),
        Product(2, "Курица", 3, 1),
    ]


def get_categories() -> List[Category]:
    return [
        Category(1, "Бакалея"),
        Category(2, "Фрукты / овощи / зелень"),
        Category(3, "Мясо / курица"),
    ]


def get_units() -> List[Unit]:
    return [
        Unit(1, "г."),
        Unit(2, "шт."),
        Unit(3, "стол. ложка"),
    ]
