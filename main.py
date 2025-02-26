from flask import Flask, abort, redirect, render_template, request, redirect
from storage import (
    get_products,
    get_product_by_id,
    get_categories,
    get_units,
    insert_product,
    update_product,
    Product,
    Category,
    Unit,
    delete_product_by_id,
    get_category_by_id,
    insert_category,
    delete_category_by_id,
    update_category,
    insert_unit,
    get_unit_by_id,
    delete_unit_by_id,
    update_unit,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_root():
    return redirect("/products")


@app.route("/products", methods=["GET"])
def get_products_route():
    view = get_products()
    return render_template("products.html", products=view)


@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_route(id: int):
    product_view = get_product_by_id(id)
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template("product.html", product=product_view)


# Создание продукта
@app.route("/products/new", methods=["GET"])
def new_product():
    return render_template("new.html", categories=get_categories(), units=get_units())


@app.route("/products/create", methods=["POST"])
def create_product():
    product_to_create = Product(
        None,
        request.form["product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    created_product_id = insert_product(product_to_create)
    return redirect(f"/products/{created_product_id}")


@app.route("/products/<int:id>/delete", methods=["GET"])
def delete_product_by_id_route(id: str):
    deleted_product_id = delete_product_by_id(id)
    if deleted_product_id is None:
        return abort(404, "Продукт не найден")
    return redirect(f"/products")


# Изменить продукт - тоже два шага
# 1 шаг - GET /products/{id}/edit - вывести заполненную форму с полями продукта с id
# 2 шаг - POST /products/{id}/update
#         сохранить изменную форму
#         редирект на GET /products/{id}


@app.route("/products/<int:id>/edit", methods=["GET"])
def edit_product_by_id(id: int):
    product_view = get_product_by_id(id)
    if product_view is None:
        return abort(404, "Продукт не найден")

    return render_template(
        "edit.html",
        product=product_view,
        categories=get_categories(),
        units=get_units(),
    )


@app.route("/products/<int:id>/update", methods=["POST"])
def update_product_route(id: int):
    product_to_update = Product(
        id,
        request.form["new_product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    updated_product_id = update_product(product_to_update)
    if updated_product_id is None:
        return abort(404, "Продукт не найден")

    return redirect(f"/products/{updated_product_id}")


# -------------------------------------------------------------------------------
# CRUD Категории


@app.route("/categories", methods=["GET"])
def get_categories_route():
    view = get_categories()
    return render_template("categories.html", categories=view)


@app.route("/categories/<int:id>", methods=["GET"])
def get_category_by_id_route(id: int):
    category_view = get_category_by_id(id)
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("category.html", category=category_view, error_flag=False)


@app.route("/categories/new", methods=["GET"])
def new_category():
    return render_template("new_category.html")


@app.route("/categories/create", methods=["POST"])
def create_category():
    category_to_create = Category(None, request.form["category_name"])
    # print(category_to_create)
    created_category_id = insert_category(category_to_create)
    return redirect(f"/categories/{created_category_id}")


@app.route("/categories/<int:id>/delete", methods=["GET"])
def delete_category_by_id_route(id: str):
    deleted_category_id = delete_category_by_id(id)
    if deleted_category_id is None:
        return abort(404, "Категория не найдена")
    if deleted_category_id == -1:
        category_view = get_category_by_id(id)
        return render_template("category.html", category=category_view, error_flag=True)
    return redirect(f"/categories")


@app.route("/categories/<int:id>/edit", methods=["GET"])
def edit_category_by_id(id: int):
    category_view = get_category_by_id(id)
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template(
        "edit_category.html",
        category=category_view,
    )


@app.route("/categories/<int:id>/update", methods=["POST"])
def update_category_route(id: int):
    category_to_update = Category(
        id,
        request.form["category_name"],
    )
    updated_category_id = update_category(category_to_update)
    if updated_category_id is None:
        return abort(404, "Категория не найдена")
    return redirect(f"/categories/{updated_category_id}")


# -------------------------------------------------------------------------------
# CRUD Units


@app.route("/units", methods=["GET"])
def get_units_route():
    view = get_units()
    print(view)
    return render_template("units.html", units=view)


@app.route("/units/new", methods=["GET"])
def new_unit():
    return render_template("new_unit.html")


@app.route("/units/create", methods=["POST"])
def create_unit():
    unit_to_create = Unit(None, request.form["unit_name"])
    created_unit_id = insert_unit(unit_to_create)
    return redirect(f"/units/{created_unit_id}")


@app.route("/units/<int:id>", methods=["GET"])
def get_unit_by_id_route(id: int):
    unit_view = get_unit_by_id(id)
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template("unit.html", unit=unit_view, error_flag=False)


@app.route("/units/<int:id>/delete", methods=["GET"])
def delete_unit_by_id_route(id: str):
    deleted_unit_id = delete_unit_by_id(id)
    if deleted_unit_id is None:
        return abort(404, "Единица измерения не найдена")
    if deleted_unit_id == -1:
        unit_view = get_unit_by_id(id)
        return render_template("unit.html", unit=unit_view, error_flag=True)
    return redirect(f"/units")


@app.route("/units/<int:id>/edit", methods=["GET"])
def edit_unit_by_id(id: int):
    unit_view = get_unit_by_id(id)
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template(
        "edit_unit.html",
        unit=unit_view,
    )


@app.route("/units/<int:id>/update", methods=["POST"])
def update_unit_route(id: int):
    unit_to_update = Unit(
        id,
        request.form["unit_name"],
    )
    updated_unit_id = update_unit(unit_to_update)
    if updated_unit_id is None:
        return abort(404, "Единица измерения не найдена")
    return redirect(f"/units/{updated_unit_id}")
