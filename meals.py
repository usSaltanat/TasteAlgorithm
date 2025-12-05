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
from forms.create_meal import MealForm
from storage import Storage
from storage_entities import Session, Meal, MealsCategory

bp = Blueprint("meals", __name__)


@bp.route("/meals", methods=["GET"])
@login_required
def get_meals_route(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_meals(session.user)
    return render_template("meals/meals.html", meals=view)


@bp.route("/meals/<int:id>", methods=["GET"])
@login_required
def get_meal_by_id_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id, session.user)
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    return render_template("meals/meal.html", meal=meal_view)


@bp.route("/meals/new", methods=["GET"])
@login_required
def new_meal(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = MealForm()
    form.products.choices = [
        (product.id, product.name) for product in storage.get_products(session.user)
    ]
    form.meals_category.choices = [
        (meals_category.id, meals_category.name)
        for meals_category in storage.get_meals_categories(session.user)
    ]
    return render_template("meals/new_meal.html", form=form)


@bp.route("/meals/create", methods=["POST"])
@login_required
def create_meal(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])
    meal_to_create = Meal(
        id=None,
        name=request.form["name"],
        meal_category=MealsCategory(int(request.form["meals_category"]), None, None),
        user=session.user,
        description=None,  # TODO прокинуть реальный description из HTTP запроса
    )
    form = MealForm(request.form)
    created_meal_id = storage.insert_meal(meal_to_create)
    if created_meal_id is None:
        flash("Не удалось создать блюдо")
        form = MealForm()
        form.meals_category.choices = [
            (meals_category.id, meals_category.name)
            for meals_category in storage.get_meals_categories(session.user)
        ]
        return render_template("meals/new_meal.html", form=form)
    storage.insert_meal_products(created_meal_id, form.products.data)
    return redirect(f"/meals/{created_meal_id}")


@bp.route("/meals/<int:id>/edit", methods=["GET"])
@login_required
def edit_meal_by_id(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    meal_view = storage.get_meal_by_id(id, session.user)
    if meal_view is None:
        return abort(404, "Блюдо не найдено")
    form = MealForm()
    form.name.data = meal_view.name
    form.meals_category.choices = [
        (meals_category.id, meals_category.name)
        for meals_category in storage.get_meals_categories(session.user)
    ]
    return render_template(
        "meals/edit_meal.html",
        meal=meal_view,
        form=form,
    )


@bp.route("/meals/<int:id>/update", methods=["POST"])
@login_required
def update_meal_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    # meal_view = storage.get_meal_by_id(id)
    meal_to_update = Meal(
        id,
        request.form["name"],
        MealsCategory(int(request.form["meals_category"]), None, None),
        session.user,
    )
    updated_meal_id = storage.update_meal(meal_to_update)
    if updated_meal_id is None:
        flash("Не удалось изменить блюдо")
        meal_view = storage.get_meal_by_id(id, session.user)
        form = MealForm()
        form.meals_category.choices = [
            (meal_category.id, meal_category.name)
            for meal_category in storage.get_meals_categories(session.user)
        ]
        return render_template(
            "meals/edit_meal.html",
            meal=meal_view,
            form=form,
        )
    return redirect(f"/meals/{updated_meal_id}")


@bp.route("/meals/<int:id>/delete", methods=["GET"])
@login_required
def delete_meal_by_id_route(id: str, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])
    deleted_meal_id = storage.delete_meal_by_id(id, session.user)
    if deleted_meal_id is None:
        flash("Не удалось удалить блюдо")
    return redirect(f"/meals")
