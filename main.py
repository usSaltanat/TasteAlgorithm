from flask import Flask, abort, redirect, render_template, request, redirect

app = Flask(__name__)

"""
CRUD = Create, Read, Update, Delete

HTTP verb: GET, POST, PUT, PATCH, DELETE

GET /products - (Read all) вывести список всех продуктов
GET /products/{id} - (Read by id) вывести один продукт по его id

Создать новый продукт - в два шага
1 шаг - GET /products/new - вывести пользователю пустую форму с полями для создаваемого продукта
2 шаг - POST /products/create -
        создать новый продукта на основании данных из формы
        редирект на страницу с продуктами, то есть GET /products

Удалить продукт
POST /products/{id}/delete
"""

products = {1: {"name": "Хлеб"}, 2: {"name": "Рис"}}


@app.route("/products", methods=["GET"])
def get_products():
    return render_template("products.html", products=products)


@app.route("/products/<string:id>", methods=["GET"])
def get_product_by_id(id: str):
    key = int(id)
    if products.get(key, None) is None:
        return abort(404, "Продукт не найден")
    return render_template("product.html", product=products[key], product_id=key)


# Создание продукта
@app.route("/products/new", methods=["GET"])
def new_product():
    return render_template("new.html")


@app.route("/products/create", methods=["POST"])
def create_product():
    next_id = max(products.keys()) + 1
    products[next_id] = {"name": request.form["product_name"]}
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
