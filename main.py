from flask import Flask, abort, redirect, render_template, request, redirect, flash
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

from forms.create_category import CategoryForm
from forms.create_unit import UnitForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"


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
    if created_product_id is None:
        flash("Не удалось создать продукт")
        return render_template(
            "new.html", categories=get_categories(), units=get_units()
        )
    return redirect(f"/products/{created_product_id}")


@app.route("/products/<int:id>/delete", methods=["GET"])
def delete_product_by_id_route(id: str):
    deleted_product_id = delete_product_by_id(id)
    if deleted_product_id is None:
        flash("Не удалось удалить продукт")
        return redirect(f"/products/{id}")
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
    product_view = get_product_by_id(id)
    product_to_update = Product(
        id,
        request.form["new_product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    updated_product_id = update_product(product_to_update)
    if updated_product_id is None:
        flash("Не удалось изменить продукт")
        # return abort(404, "Продукт не найден")
        return render_template(
            "edit.html",
            product=product_view,
            categories=get_categories(),
            units=get_units(),
        )
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
    return render_template("category.html", category=category_view)


@app.route("/categories/new", methods=["GET"])
def new_category():
    form = CategoryForm()
    return render_template("new_category.html", form=form)


@app.route("/categories/create", methods=["POST"])
def create_category():
    form = CategoryForm(request.form)
    if not form.validate():
        return render_template("new_category.html", form=form)
    category_to_create = Category(None, form.category.data)
    created_category_id = insert_category(category_to_create)
    if created_category_id is None:
        flash("Не удалось создать категорию")
        return render_template("new_category.html", form=form)
    return redirect(f"/categories/{created_category_id}")


@app.route("/categories/<int:id>/delete", methods=["GET"])
def delete_category_by_id_route(id: str):
    deleted_category_id = delete_category_by_id(id)
    if deleted_category_id is None:
        flash("Не удалось удалить категорию")
        return redirect(f"/categories/{id}")
    return redirect(f"/categories")


@app.route("/categories/<int:id>/edit", methods=["GET"])
def edit_category_by_id(id: int):
    category_view = get_category_by_id(id)
    form = CategoryForm()
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("edit_category.html", category=category_view, form=form)


@app.route("/categories/<int:id>/update", methods=["POST"])
def update_category_route(id: int):
    form = CategoryForm(request.form)
    category_view = get_category_by_id(id)
    if not form.validate():
        return render_template("edit_category.html", category=category_view, form=form)
    category_to_update = Category(
        id,
        form.category.data,
    )
    updated_category_id = update_category(category_to_update)
    if updated_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию")
        return render_template("edit_category.html", category=category_view, form=form)
    return redirect(f"/categories/{updated_category_id}")


# -------------------------------------------------------------------------------
# CRUD Units


@app.route("/units", methods=["GET"])
def get_units_route():
    view = get_units()
    return render_template("units.html", units=view)


@app.route("/units/new", methods=["GET"])
def new_unit():
    form = UnitForm()
    return render_template("new_unit.html", form=form)


@app.route("/units/create", methods=["POST"])
def create_unit():
    form = UnitForm(request.form)
    if not form.validate():
        return render_template("new_unit.html", form=form)
    unit_to_create = Unit(None, form.unit.data)
    created_unit_id = insert_unit(unit_to_create)
    if created_unit_id is None:
        flash("Не удалось создать единицу измерения")
        return render_template("new_unit.html", form=form)
    return redirect(f"/units/{created_unit_id}")


@app.route("/units/<int:id>", methods=["GET"])
def get_unit_by_id_route(id: int):
    unit_view = get_unit_by_id(id)
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template("unit.html", unit=unit_view)


@app.route("/units/<int:id>/delete", methods=["GET"])
def delete_unit_by_id_route(id: str):
    deleted_unit_id = delete_unit_by_id(id)
    if deleted_unit_id is None:
        flash("Не удалось удалить единицу измерения")
        return redirect(f"/units/{id}")
    return redirect(f"/units")


@app.route("/units/<int:id>/edit", methods=["GET"])
def edit_unit_by_id(id: int):
    unit_view = get_unit_by_id(id)
    form = UnitForm(request.form)
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template(
        "edit_unit.html",
        unit=unit_view,
        form=form,
    )


@app.route("/units/<int:id>/update", methods=["POST"])
def update_unit_route(id: int):
    form = UnitForm(request.form)
    unit_view = get_unit_by_id(id)
    if not form.validate():
        return render_template("edit_unit.html", unit=unit_view, form=form)
    unit_to_update = Unit(
        id,
        form.unit.data,
    )
    updated_unit_id = update_unit(unit_to_update)
    if updated_unit_id is None:
        flash("Не удалось изменить единицу измерения")
        return render_template("edit_unit.html", unit=unit_view, form=form)
    return redirect(f"/units/{updated_unit_id}")
