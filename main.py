from flask import (
    Flask,
    redirect,
)

from auth import bp as auth_bp, login_required
from products import bp as products_bp
from meals_categories import bp as meals_categories_bp
from categories import bp as categories_bp
from units import bp as units_bp
from meals import bp as meals_bp
from menu import bp as menu_bp
from storage import Storage
from storage_entities import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"
app.config["storage"] = Storage()

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(meals_categories_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(units_bp)
app.register_blueprint(meals_bp)
app.register_blueprint(menu_bp)


@app.route("/", methods=["GET"])
@login_required
def get_root(session: Session):
    # print(f"❗️user = {pbkdf2_sha256.hash("qwerty123")}")
    return redirect("/products")


# -------------------------------------------------------------------------------
# CRUD recipes


# @app.route("/recipes", methods=["GET"])
# @login_required
# def get_recipes_route():
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     view = storage.get_recipes()
#     return render_template("recipes/recipes.html", recipes=view)


# @app.route("/recipes/<int:id>", methods=["GET"])
# @login_required
# def get_recipe_by_id_route(id: int):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     recipe_view = storage.get_recipe_by_id(id)
#     if recipe_view is None:
#         return abort(404, "Рецепт не найден")
#     return render_template("recipes/recipe.html", recipe=recipe_view)


# @app.route("/recipes/new", methods=["GET"])
# @login_required
# def new_recipe():
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     form = RecipeForm()
#     form.meal.choices = [
#         (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
#     ]
#     return render_template("recipes/new_recipe.html", form=form)


# @app.route("/recipes/create", methods=["POST"])
# @login_required
# def create_recipe():
#     storage = typing.cast(Storage, current_app.config["storage"])
#     recipe_to_create = Recipe(
#         None,
#         Meal(int(request.form["meal"]), None, MealsCategory(None, None)),
#         request.form["recipe_body"],
#     )
#     created_recipe_id = storage.insert_recipe(recipe_to_create)
#     if created_recipe_id is None:
#         flash("Не удалось создать рецепт")
#         form = RecipeForm()
#         form.meal.choices = [
#             (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
#         ]
#         return render_template("recipes/new_recipe.html", form=form)
#     return redirect(f"/recipes/{created_recipe_id}")


# @app.route("/recipes/<int:id>/edit", methods=["GET"])
# @login_required
# def edit_recipe_by_id(id: int):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     recipe_view = storage.get_recipe_by_id(id)
#     form = RecipeForm()
#     form.meal.choices = [
#         (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
#     ]
#     if recipe_view is None:
#         return abort(404, "Рецепт не найден")
#     return render_template(
#         "recipes/edit_recipe.html",
#         recipe=recipe_view,
#         form=form,
#     )


# @app.route("/recipes/<int:id>/update", methods=["POST"])
# @login_required
# def update_recipe_route(id: int):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     recipe_to_update = Recipe(
#         id,
#         Meal(int(request.form["meal"]), None, MealsCategory(None, None)),
#         request.form["recipe_body"],
#     )
#     updated_recipe_id = storage.update_recipe(recipe_to_update)
#     if updated_recipe_id is None:
#         flash("Не удалось изменить рецепт")
#         recipe_view = storage.get_recipe_by_id(id)
#         form = RecipeForm()
#         form.meal.choices = [
#             (recipe.meal.id, recipe.meal.name) for recipe in storage.get_recipes()
#         ]
#         return render_template(
#             "recipes/edit_recipe.html",
#             recipe=recipe_view,
#             form=form,
#         )
#     return redirect(f"/recipes/{updated_recipe_id}")


# @app.route("/recipes/<int:id>/delete", methods=["GET"])
# @login_required
# def delete_recipe_by_id_route(id: str):
#     storage = typing.cast(Storage, current_app.config["storage"])
#     deleted_recipe_id = storage.delete_recipe_by_id(id)
#     if deleted_recipe_id is None:
#         flash("Не удалось удалить рецепт")
#     return redirect(f"/recipes")
