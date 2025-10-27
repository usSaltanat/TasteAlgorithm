import typing

from flask import (
    Blueprint,
    current_app,
    render_template,
    abort,
    request,
    flash,
    redirect,
)

from auth import login_required
from forms.create_meals_category import MealsCategoryForm
from storage import Storage
from storage_entities import Session, MealsCategory

bp = Blueprint("meals_categories", __name__)


# @bp.route("/meals_categories", methods=["GET"])
# @login_required
# def get_meals_categories_route(session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     view = storage.get_meals_categories(session.user)
#     return render_template(
#         "meals_categories/meals_categories.html", meals_categories=view
#     )


# @bp.route("/meals_categories/<int:id>", methods=["GET"])
# @login_required
# def get_meals_category_by_id_route(id: int, session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     meals_category_view = storage.get_meals_category_by_id(id, session.user)
#     if meals_category_view is None:
#         return abort(404, "Категория блюда не найдена")
#     return render_template(
#         "meals_categories/meals_category.html", meals_category=meals_category_view
#     )


# @bp.route("/meals_categories/new", methods=["GET"])
# @login_required
# def new_meals_category(session: Session):
#     form = MealsCategoryForm()
#     return render_template("meals_categories/new_meals_category.html", form=form)


# @bp.route("/meals_categories/create", methods=["POST"])
# @login_required
# def create_meal_categories(session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     form = MealsCategoryForm(request.form)
#     if not form.validate():
#         return render_template("meals_categories/new_meals_category.html", form=form)
#     meals_category_to_create = MealsCategory(
#         None, form.meals_category.data, session.user
#     )
#     created_meals_category_id = storage.insert_meals_category(meals_category_to_create)
#     if created_meals_category_id is None:
#         flash("Не удалось создать категорию блюда")
#         return render_template("meals_categories/new_meals_category.html", form=form)
#     return redirect(f"/meals_categories/{created_meals_category_id}")


# @bp.route("/meals_categories/<int:id>/edit", methods=["GET"])
# @login_required
# def edit_meals_category_by_id(id: int, session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     meals_category_view = storage.get_meals_category_by_id(id, session.user)
#     if meals_category_view is None:
#         return abort(404, "Категория блюда не найдена")
#     form = MealsCategoryForm()
#     form.meals_category.data = meals_category_view.name
#     return render_template(
#         "meals_categories/edit_meals_category.html",
#         meals_category=meals_category_view,
#         form=form,
#     )


# @bp.route("/meals_categories/<int:id>/update", methods=["POST"])
# @login_required
# def update_meals_category_route(id: int, session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     form = MealsCategoryForm(request.form)
#     meals_category_view = storage.get_meals_category_by_id(id, session.user)
#     if not form.validate():
#         return render_template(
#             "meals_categories/edit_meals_category.html",
#             meals_category=meals_category_view,
#             form=form,
#         )
#     meals_category_to_update = MealsCategory(id, form.meals_category.data, session.user)
#     updated_meals_category_id = storage.update_meals_category(meals_category_to_update)
#     if updated_meals_category_id is None:  # обход случая когда категории повторяются
#         flash("Не удалось изменить категорию блюда")
#         return render_template(
#             "meals_categories/edit_meals_category.html",
#             meals_category=meals_category_view,
#             form=form,
#         )
#     return redirect(f"/meals_categories/{updated_meals_category_id}")


# @bp.route("/meals_categories/<int:id>/delete", methods=["GET"])
# @login_required
# def delete_meals_category_by_id_route(id: str, session: Session):
#     storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
#     deleted_meals_category_id = storage.delete_meals_category_by_id(id, session.user)
#     if deleted_meals_category_id is None:
#         flash("Не удалось удалить категорию блюда")
#     return redirect(f"/meals_categories")
