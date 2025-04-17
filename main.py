from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    redirect,
    flash,
    current_app,
)
from storage import Storage, Product, Category, Unit, MealsCategory, Meal
import typing

from forms.create_category import CategoryForm
from forms.create_unit import UnitForm
from forms.create_meals_category import MealsCategoryForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"
app.config["storage"] = Storage()


@app.route("/", methods=["GET"])
def get_root():
    return redirect("/products")


@app.route("/products", methods=["GET"])
def get_products_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_products()
    return render_template("products.html", products=view)


@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id)
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template("product.html", product=product_view)


# Создание продукта
@app.route("/products/new", methods=["GET"])
def new_product():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    return render_template(
        "new.html", categories=storage.get_categories(), units=storage.get_units()
    )


@app.route("/products/create", methods=["POST"])
def create_product():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_to_create = Product(
        None,
        request.form["product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    created_product_id = storage.insert_product(product_to_create)
    if created_product_id is None:
        flash("Не удалось создать продукт")
        return render_template(
            "new.html", categories=storage.get_categories(), units=storage.get_units()
        )
    return redirect(f"/products/{created_product_id}")


@app.route("/products/<int:id>/delete", methods=["GET"])
def delete_product_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_product_id = storage.delete_product_by_id(id)
    if deleted_product_id is None:
        flash("Не удалось удалить продукт")
    return redirect(f"/products")


@app.route("/products/<int:id>/edit", methods=["GET"])
def edit_product_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id)
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template(
        "edit.html",
        product=product_view,
        categories=storage.get_categories(),
        units=storage.get_units(),
    )


@app.route("/products/<int:id>/update", methods=["POST"])
def update_product_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id)
    product_to_update = Product(
        id,
        request.form["new_product_name"],
        Category(request.form["product_category_id"], None),
        Unit(request.form["product_unit_id"], None),
    )
    updated_product_id = storage.update_product(product_to_update)
    if updated_product_id is None:
        flash("Не удалось изменить продукт")
        # return abort(404, "Продукт не найден")
        return render_template(
            "edit.html",
            product=product_view,
            categories=storage.get_categories(),
            units=storage.get_units(),
        )
    return redirect(f"/products/{updated_product_id}")


# -------------------------------------------------------------------------------
# CRUD Категории


@app.route("/categories", methods=["GET"])
def get_categories_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_categories()
    return render_template("categories.html", categories=view)


@app.route("/categories/<int:id>", methods=["GET"])
def get_category_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    category_view = storage.get_category_by_id(id)
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("category.html", category=category_view)


@app.route("/categories/new", methods=["GET"])
def new_category():
    form = CategoryForm()
    return render_template("new_category.html", form=form)


@app.route("/categories/create", methods=["POST"])
def create_category():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    if not form.validate():
        return render_template("new_category.html", form=form)
    category_to_create = Category(None, form.category.data)
    created_category_id = storage.insert_category(category_to_create)
    if created_category_id is None:
        flash("Не удалось создать категорию")
        return render_template("new_category.html", form=form)
    return redirect(f"/categories/{created_category_id}")


@app.route("/categories/<int:id>/delete", methods=["GET"])
def delete_category_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_category_id = storage.delete_category_by_id(id)
    if deleted_category_id is None:
        flash("Не удалось удалить категорию")
        # return redirect(f"/categories/{id}")
    return redirect(f"/categories")


@app.route("/categories/<int:id>/edit", methods=["GET"])
def edit_category_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    category_view = storage.get_category_by_id(id)
    form = CategoryForm()
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("edit_category.html", category=category_view, form=form)


@app.route("/categories/<int:id>/update", methods=["POST"])
def update_category_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    category_view = storage.get_category_by_id(id)
    if not form.validate():
        return render_template("edit_category.html", category=category_view, form=form)
    category_to_update = Category(
        id,
        form.category.data,
    )
    updated_category_id = storage.update_category(category_to_update)
    if updated_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию")
        return render_template("edit_category.html", category=category_view, form=form)
    return redirect(f"/categories/{updated_category_id}")


# -------------------------------------------------------------------------------
# CRUD Units


@app.route("/units", methods=["GET"])
def get_units_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_units()
    return render_template("units.html", units=view)


@app.route("/units/new", methods=["GET"])
def new_unit():
    form = UnitForm()
    return render_template("new_unit.html", form=form)


@app.route("/units/create", methods=["POST"])
def create_unit():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = UnitForm(request.form)
    if not form.validate():
        return render_template("new_unit.html", form=form)
    unit_to_create = Unit(None, form.unit.data)
    created_unit_id = storage.insert_unit(unit_to_create)
    if created_unit_id is None:
        flash("Не удалось создать еденицу измерения")
        return render_template("new_unit.html", form=form)
    return redirect(f"/units/{created_unit_id}")


@app.route("/units/<int:id>", methods=["GET"])
def get_unit_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    if unit_view is None:
        return abort(404, "Еденица измерения не найдена")
    return render_template("unit.html", unit=unit_view)


@app.route("/units/<int:id>/delete", methods=["GET"])
def delete_unit_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_unit_id = storage.delete_unit_by_id(id)
    if deleted_unit_id is None:
        flash("Не удалось удалить еденицу измерения")
        # return redirect(f"/units/{id}")
    return redirect(f"/units")


@app.route("/units/<int:id>/edit", methods=["GET"])
def edit_unit_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    form = UnitForm(request.form)
    if unit_view is None:
        return abort(404, "Еденица измерения не найдена")
    return render_template(
        "edit_unit.html",
        unit=unit_view,
        form=form,
    )


@app.route("/units/<int:id>/update", methods=["POST"])
def update_unit_route(id: int):
    form = UnitForm(request.form)
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    if not form.validate():
        return render_template("edit_unit.html", unit=unit_view, form=form)
    unit_to_update = Unit(
        id,
        form.unit.data,
    )
    updated_unit_id = storage.update_unit(unit_to_update)
    if updated_unit_id is None:
        flash("Не удалось изменить еденицу измерения")
        return render_template("edit_unit.html", unit=unit_view, form=form)
    return redirect(f"/units/{updated_unit_id}")


# -------------------------------------------------------------------------------
# CRUD meals_category


@app.route("/meals_categories", methods=["GET"])
def get_meals_categories_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_meals_categories()
    return render_template("meals_categories.html", meals_categories=view)


@app.route("/meals_categories/<int:id>", methods=["GET"])
def get_meals_category_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meals_category_view = storage.get_meals_category_by_id(id)
    if meals_category_view is None:
        return abort(404, "Категория блюда не найдена")
    return render_template("meals_category.html", meals_category=meals_category_view)


@app.route("/meals_categories/new", methods=["GET"])
def new_meals_category():
    form = MealsCategoryForm()
    return render_template("new_meals_category.html", form=form)


@app.route("/meals_categories/create", methods=["POST"])
def create_meal_categories():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealsCategoryForm(request.form)
    if not form.validate():
        return render_template("new_meals_category.html", form=form)
    meals_category_to_create = MealsCategory(None, form.meals_category.data)
    created_meals_category_id = storage.insert_meals_category(meals_category_to_create)
    if created_meals_category_id is None:
        flash("Не удалось создать категорию блюда")
        return render_template("new_meals_category.html", form=form)
    return redirect(f"/meals_categories/{created_meals_category_id}")


@app.route("/meals_categories/<int:id>/edit", methods=["GET"])
def edit_meals_category_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meals_category_view = storage.get_meals_category_by_id(id)
    form = MealsCategoryForm()
    if meals_category_view is None:
        return abort(404, "Категория блюда не найдена")
    return render_template(
        "edit_meals_category.html", meals_category=meals_category_view, form=form
    )


@app.route("/meals_categories/<int:id>/update", methods=["POST"])
def update_meals_category_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealsCategoryForm(request.form)
    meals_category_view = storage.get_meals_category_by_id(id)
    if not form.validate():
        return render_template(
            "edit_meals_category.html", meals_category=meals_category_view, form=form
        )
    print("!!!", form.meals_category.data)
    meals_category_to_update = MealsCategory(
        id,
        form.meals_category.data,
    )
    updated_meals_category_id = storage.update_meals_category(meals_category_to_update)
    if updated_meals_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию блюда")
        return render_template(
            "edit_meals_category.html", meals_category=meals_category_view, form=form
        )
    return redirect(f"/meals_categories/{updated_meals_category_id}")


@app.route("/meals_categories/<int:id>/delete", methods=["GET"])
def delete_meals_category_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_meals_category_id = storage.delete_meals_category_by_id(id)
    if deleted_meals_category_id is None:
        flash("Не удалось удалить категорию блюда")
    return redirect(f"/meals_categories")


# -------------------------------------------------------------------------------
# CRUD meals


@app.route("/meals", methods=["GET"])
def get_meals_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_meals()
    return render_template("meals.html", meals=view)


@app.route("/meals/<int:id>", methods=["GET"])
def get_meal_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id)
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    return render_template("meal.html", meal=meal_view)


@app.route("/meals/new", methods=["GET"])
def new_meal():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    return render_template(
        "new_meal.html", meals_categories=storage.get_meals_categories()
    )


@app.route("/meals/create", methods=["POST"])
def create_meal():
    storage = typing.cast(Storage, current_app.config["storage"])
    meal_to_create = Meal(
        None,
        request.form["meal_name"],
        MealsCategory(request.form["meal_category_id"], None),
    )
    created_meal_id = storage.insert_meal(meal_to_create)
    if created_meal_id is None:
        flash("Не удалось создать блюдо")
        return render_template(
            "new_meal.html", meals_categories=storage.get_meals_categories()
        )
    return redirect(f"/meals/{created_meal_id}")


@app.route("/meals/<int:id>/edit", methods=["GET"])
def edit_meal_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id)
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    return render_template(
        "edit_meal.html",
        meal=meal_view,
        categories=storage.get_meals_categories(),
    )


@app.route("/meals/<int:id>/delete", methods=["GET"])
def delete_meal_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])
    deleted_meal_id = storage.delete_meal_by_id(id)
    if deleted_meal_id is None:
        flash("Не удалось удалить блюдо")
    return redirect(f"/meals")
