from flask import Flask, abort, redirect, render_template, request, redirect
from storage import (
    get_products,
    get_product_by_id,
    get_categories,
    get_units,
    insert_product,
    Product,
    Category,
    Unit,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_root():
    return redirect("/products")


@app.route("/products", methods=["GET"])
def get_products_route():
    view = get_products()
    return render_template("products.html", products=view)


@app.route("/products/<string:id>", methods=["GET"])
def get_product_by_id_route(id: str):
    view = get_product_by_id(id)
    if view[0].id == None:
        return abort(404, "Продукт не найден")
    return render_template("product.html", product=view, product_id=id)


# Создание продукта
@app.route("/products/new", methods=["GET"])
def new_product():
    return render_template("new.html", categories=get_categories(), units=get_units())


@app.route("/products/create", methods=["POST"])
def create_product():
    created_product = Product(
        None,
        request.form["product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    next_id = insert_product(created_product)
    return redirect(f"/products/{next_id}")


@app.route("/products/<int:id>/delete", methods=["GET"])
def delete_product_by_id(id: str):
    key = int(id)
    if products.get(key, None) is None:
        return abort(404, "Продукт не найден")
    else:
        del products[key]
    return redirect(f"/products")


# Изменить продукт - тоже два шага
# 1 шаг - GET /products/{id}/edit - вывести заполненную форму с полями продукта с id
# 2 шаг - POST /products/{id}/update
#         сохранить изменную форму
#         редирект на GET /products/{id}


@app.route("/products/<int:id>/edit", methods=["GET"])
def edit_product_by_id(id: str):
    key = int(id)
    return render_template("edit.html", product=products[key], product_id=key)


@app.route("/products/<int:id>/update", methods=["POST"])
def update_product(id: str):
    key = int(id)
    products[key] = {"name": request.form["new_product_name"]}
    return redirect(f"/products/{key}")
