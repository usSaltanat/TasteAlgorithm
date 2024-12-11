from typing import List, NamedTuple
from storage import Product, Category, Unit, get_categories, get_products, get_units


class ProductView(NamedTuple):
    id: int
    name: str
    category: str
    unit: str


def get_product_category(product: Product) -> Category:
    categories = list(
        filter(
            lambda category: category.id == product.category_id,
            get_categories(),
        )
    )
    assert len(categories) == 1
    catetegory = categories[0]
    return catetegory


def get_product_unit(product: Product) -> Unit:
    units = list(
        filter(
            lambda unit: unit.id == product.unit_id,
            get_units(),
        )
    )
    assert len(units) == 1
    unit = units[0]
    return unit


def get_products_view() -> List[ProductView]:
    def fn(product: Product) -> ProductView:
        return ProductView(
            id=product.id,
            name=product.name,
            category=get_product_category(product).name,
            unit=get_product_unit(product).name,
        )

    return map(
        fn,
        get_products(),
    )
