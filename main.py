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
from storage import Storage, Product, Category, Unit, MealsCategory, Meal, Recipe
import typing

from forms.create_category import CategoryForm
from forms.create_unit import UnitForm
from forms.create_meals_category import MealsCategoryForm
from forms.create_product import ProductForm
from forms.create_meal import MealForm
from forms.create_recipe import RecipeForm

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
    return render_template("products/products.html", products=view)


@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id)
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template("products/product.html", product=product_view)


# Создание продукта
@app.route("/products/new", methods=["GET"])
def new_product():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = ProductForm()
    form.category.choices = [
        (category.id, category.name) for category in storage.get_categories()
    ]
    form.unit.choices = [(unit.id, unit.name) for unit in storage.get_units()]
    return render_template(
        "products/new.html",
        form=form,
    )


@app.route("/products/create", methods=["POST"])
def create_product():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_to_create = Product(
        None,
        request.form["name"],
        Category(int(request.form["category"]), None),
        Unit(int(request.form["unit"]), None),
    )
    created_product_id = storage.insert_product(product_to_create)
    if created_product_id is None:
        flash("Не удалось создать продукт")
        form = ProductForm()
        form.category.choices = [
            (category.id, category.name) for category in storage.get_categories()
        ]
        form.unit.choices = [(unit.id, unit.name) for unit in storage.get_units()]
        return render_template(
            "products/new.html",
            form=form,
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
    form = ProductForm()
    form.category.choices = [
        (category.id, category.name) for category in storage.get_categories()
    ]
    form.unit.choices = [(unit.id, unit.name) for unit in storage.get_units()]
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template(
        "products/edit.html",
        product=product_view,
        form=form,
    )


@app.route("/products/<int:id>/update", methods=["POST"])
def update_product_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id)
    product_to_update = Product(
        id,
        request.form["name"],
        Category(int(request.form["category"]), None),
        Unit(int(request.form["unit"]), None),
    )
    updated_product_id = storage.update_product(product_to_update)
    if updated_product_id is None:
        flash("Не удалось изменить продукт")
        product_view = storage.get_product_by_id(id)
        form = ProductForm()
        form.category.choices = [
            (category.id, category.name) for category in storage.get_categories()
        ]
        form.unit.choices = [(unit.id, unit.name) for unit in storage.get_units()]
        return render_template(
            "products/edit.html",
            product=product_view,
            form=form,
        )
    return redirect(f"/products/{updated_product_id}")


# -------------------------------------------------------------------------------
# CRUD Категории


@app.route("/categories", methods=["GET"])
def get_categories_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_categories()
    return render_template("categories/categories.html", categories=view)


@app.route("/categories/<int:id>", methods=["GET"])
def get_category_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    category_view = storage.get_category_by_id(id)
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("categories/category.html", category=category_view)


@app.route("/categories/new", methods=["GET"])
def new_category():
    form = CategoryForm()
    return render_template("categories/new_category.html", form=form)


@app.route("/categories/create", methods=["POST"])
def create_category():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    if not form.validate():
        return render_template("categories/new_category.html", form=form)
    category_to_create = Category(None, form.category.data)
    created_category_id = storage.insert_category(category_to_create)
    if created_category_id is None:
        flash("Не удалось создать категорию")
        return render_template("categories/new_category.html", form=form)
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
    return render_template(
        "categories/edit_category.html", category=category_view, form=form
    )


@app.route("/categories/<int:id>/update", methods=["POST"])
def update_category_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    category_view = storage.get_category_by_id(id)
    if not form.validate():
        return render_template(
            "categories/edit_category.html", category=category_view, form=form
        )
    category_to_update = Category(
        id,
        form.category.data,
    )
    updated_category_id = storage.update_category(category_to_update)
    if updated_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию")
        return render_template(
            "categories/edit_category.html", category=category_view, form=form
        )
    return redirect(f"/categories/{updated_category_id}")


# -------------------------------------------------------------------------------
# CRUD Units


@app.route("/units", methods=["GET"])
def get_units_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_units()
    return render_template("units/units.html", units=view)


@app.route("/units/new", methods=["GET"])
def new_unit():
    form = UnitForm()
    return render_template("units/new_unit.html", form=form)


@app.route("/units/create", methods=["POST"])
def create_unit():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = UnitForm(request.form)
    if not form.validate():
        return render_template("units/new_unit.html", form=form)
    unit_to_create = Unit(None, form.unit.data)
    created_unit_id = storage.insert_unit(unit_to_create)
    if created_unit_id is None:
        flash("Не удалось создать еденицу измерения")
        return render_template("units/new_unit.html", form=form)
    return redirect(f"/units/{created_unit_id}")


@app.route("/units/<int:id>", methods=["GET"])
def get_unit_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    if unit_view is None:
        return abort(404, "Еденица измерения не найдена")
    return render_template("units/unit.html", unit=unit_view)


@app.route("/units/<int:id>/delete", methods=["GET"])
def delete_unit_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_unit_id = storage.delete_unit_by_id(id)
    if deleted_unit_id is None:
        flash("Не удалось удалить еденицу измерения")
    return redirect(f"/units")


@app.route("/units/<int:id>/edit", methods=["GET"])
def edit_unit_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    form = UnitForm(request.form)
    if unit_view is None:
        return abort(404, "Еденица измерения не найдена")
    return render_template(
        "units/edit_unit.html",
        unit=unit_view,
        form=form,
    )


@app.route("/units/<int:id>/update", methods=["POST"])
def update_unit_route(id: int):
    form = UnitForm(request.form)
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id)
    if not form.validate():
        return render_template("units/edit_unit.html", unit=unit_view, form=form)
    unit_to_update = Unit(
        id,
        form.unit.data,
    )
    updated_unit_id = storage.update_unit(unit_to_update)
    if updated_unit_id is None:
        flash("Не удалось изменить еденицу измерения")
        return render_template("units/edit_unit.html", unit=unit_view, form=form)
    return redirect(f"/units/{updated_unit_id}")


# -------------------------------------------------------------------------------
# CRUD meals_category


@app.route("/meals_categories", methods=["GET"])
def get_meals_categories_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_meals_categories()
    return render_template(
        "meals_categories/meals_categories.html", meals_categories=view
    )


@app.route("/meals_categories/<int:id>", methods=["GET"])
def get_meals_category_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meals_category_view = storage.get_meals_category_by_id(id)
    if meals_category_view is None:
        return abort(404, "Категория блюда не найдена")
    return render_template(
        "meals_categories/meals_category.html", meals_category=meals_category_view
    )


@app.route("/meals_categories/new", methods=["GET"])
def new_meals_category():
    form = MealsCategoryForm()
    return render_template("meals_categories/new_meals_category.html", form=form)


@app.route("/meals_categories/create", methods=["POST"])
def create_meal_categories():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealsCategoryForm(request.form)
    if not form.validate():
        return render_template("meals_categories/new_meals_category.html", form=form)
    meals_category_to_create = MealsCategory(None, form.meals_category.data)
    created_meals_category_id = storage.insert_meals_category(meals_category_to_create)
    if created_meals_category_id is None:
        flash("Не удалось создать категорию блюда")
        return render_template("meals_categories/new_meals_category.html", form=form)
    return redirect(f"/meals_categories/{created_meals_category_id}")


@app.route("/meals_categories/<int:id>/edit", methods=["GET"])
def edit_meals_category_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meals_category_view = storage.get_meals_category_by_id(id)
    form = MealsCategoryForm()
    if meals_category_view is None:
        return abort(404, "Категория блюда не найдена")
    return render_template(
        "meals_categories/edit_meals_category.html",
        meals_category=meals_category_view,
        form=form,
    )


@app.route("/meals_categories/<int:id>/update", methods=["POST"])
def update_meals_category_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealsCategoryForm(request.form)
    meals_category_view = storage.get_meals_category_by_id(id)
    if not form.validate():
        return render_template(
            "meals_categories/edit_meals_category.html",
            meals_category=meals_category_view,
            form=form,
        )
    meals_category_to_update = MealsCategory(
        id,
        form.meals_category.data,
    )
    updated_meals_category_id = storage.update_meals_category(meals_category_to_update)
    if updated_meals_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию блюда")
        return render_template(
            "meals_categories/edit_meals_category.html",
            meals_category=meals_category_view,
            form=form,
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
    return render_template("meals/meals.html", meals=view)


@app.route("/meals/<int:id>", methods=["GET"])
def get_meal_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id)
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    return render_template("meals/meal.html", meal=meal_view)


@app.route("/meals/new", methods=["GET"])
def new_meal():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealForm()
    form.meals_category.choices = [
        (meals_category.id, meals_category.name)
        for meals_category in storage.get_meals_categories()
    ]
    return render_template("meals/new_meal.html", form=form)


@app.route("/meals/create", methods=["POST"])
def create_meal():
    storage = typing.cast(Storage, current_app.config["storage"])
    meal_to_create = Meal(
        None,
        request.form["name"],
        MealsCategory(int(request.form["meals_category"]), None),
    )
    created_meal_id = storage.insert_meal(meal_to_create)
    if created_meal_id is None:
        flash("Не удалось создать блюдо")
        form = MealForm()
        form.meals_category.choices = [
            (meals_category.id, meals_category.name)
            for meals_category in storage.get_meals_categories()
        ]
        return render_template("meals/new_meal.html", form=form)
    return redirect(f"/meals/{created_meal_id}")


@app.route("/meals/<int:id>/edit", methods=["GET"])
def edit_meal_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id)
    form = MealForm()
    form.meals_category.choices = [
        (meals_category.id, meals_category.name)
        for meals_category in storage.get_meals_categories()
    ]
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    return render_template(
        "meals/edit_meal.html",
        meal=meal_view,
        form=form,
    )


@app.route("/meals/<int:id>/update", methods=["POST"])
def update_meal_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    # meal_view = storage.get_meal_by_id(id)
    meal_to_update = Meal(
        id,
        request.form["name"],
        MealsCategory(int(request.form["meals_category"]), None),
    )
    updated_meal_id = storage.update_meal(meal_to_update)
    if updated_meal_id is None:
        flash("Не удалось изменить блюдо")
        meal_view = storage.get_meal_by_id(id)
        form = MealForm()
        form.meals_category.choices = [
            (meal_category.id, meal_category.name)
            for meal_category in storage.get_meals_categories()
        ]
        return render_template(
            "meals/edit_meal.html",
            meal=meal_view,
            form=form,
        )
    return redirect(f"/meals/{updated_meal_id}")


@app.route("/meals/<int:id>/delete", methods=["GET"])
def delete_meal_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])
    deleted_meal_id = storage.delete_meal_by_id(id)
    if deleted_meal_id is None:
        flash("Не удалось удалить блюдо")
    return redirect(f"/meals")


# -------------------------------------------------------------------------------
# CRUD recipes


@app.route("/recipes", methods=["GET"])
def get_recipes_route():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_recipes()
    return render_template("recipes/recipes.html", recipes=view)


@app.route("/recipes/<int:id>", methods=["GET"])
def get_recipe_by_id_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    recipe_view = storage.get_recipe_by_id(id)
    if recipe_view is None:
        return abort(404, "Рецепт не найден")
    return render_template("recipes/recipe.html", recipe=recipe_view)


@app.route("/recipes/new", methods=["GET"])
def new_recipe():
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = RecipeForm()
    form.meal.choices = [
        (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
    ]
    return render_template("recipes/new_recipe.html", form=form)


@app.route("/recipes/create", methods=["POST"])
def create_recipe():
    storage = typing.cast(Storage, current_app.config["storage"])
    recipe_to_create = Recipe(
        None,
        Meal(int(request.form["meal"]), None, MealsCategory(None, None)),
        request.form["recipe_body"],
    )
    created_recipe_id = storage.insert_recipe(recipe_to_create)
    if created_recipe_id is None:
        flash("Не удалось создать рецепт")
        form = RecipeForm()
        form.meal.choices = [
            (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
        ]
        return render_template("recipes/new_recipe.html", form=form)
    return redirect(f"/recipes/{created_recipe_id}")


@app.route("/recipes/<int:id>/edit", methods=["GET"])
def edit_recipe_by_id(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    recipe_view = storage.get_recipe_by_id(id)
    form = RecipeForm()
    form.meal.choices = [
        (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
    ]
    if recipe_view is None:
        return abort(404, "Рецепт не найден")
    return render_template(
        "recipes/edit_recipe.html",
        recipe=recipe_view,
        form=form,
    )


@app.route("/recipes/<int:id>/update", methods=["POST"])
def update_recipe_route(id: int):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    recipe_to_update = Recipe(
        id,
        Meal(int(request.form["meal"]), None, MealsCategory(None, None)),
        request.form["recipe_body"],
    )
    updated_recipe_id = storage.update_recipe(recipe_to_update)
    if updated_recipe_id is None:
        flash("Не удалось изменить рецепт")
        recipe_view = storage.get_recipe_by_id(id)
        form = RecipeForm()
        form.meal.choices = [
            (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
        ]
        return render_template(
            "recipes/edit_recipe.html",
            recipe=recipe_view,
            form=form,
        )
    return redirect(f"/recipes/{updated_recipe_id}")


@app.route("/recipes/<int:id>/delete", methods=["GET"])
def delete_recipe_by_id_route(id: str):
    storage = typing.cast(Storage, current_app.config["storage"])
    deleted_recipe_id = storage.delete_recipe_by_id(id)
    if deleted_recipe_id is None:
        flash("Не удалось удалить рецепт")
    return redirect(f"/recipes")
