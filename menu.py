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
from forms.create_menu import DailyMenuForm, WeeklyMenuForm
from storage import Storage
from storage_entities import Session, Product, Category, Unit, User

bp = Blueprint("menu", __name__)


@bp.route("/test")
def test():
    return "Blueprint is working!"


@bp.route("/menu", methods=["GET"])
@login_required
def create_menu(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = WeeklyMenuForm()
    # Получаем данные из базы
    breakfast_choices = [(meal.id, meal.name) for meal in storage.get_meals_by_category(session.user, 1)]
    lunch_choices = [(meal.id, meal.name) for meal in storage.get_meals_by_category(session.user, 2)]
    dinner_choices = [(meal.id, meal.name) for meal in storage.get_meals_by_category(session.user, 3)]
    snack_choices = [(meal.id, meal.name) for meal in storage.get_meals_by_category(session.user, 4)]
    
    # Заполняем choices для каждого дня
    for day_form in form.days:
        day_form.breakfast.choices = [('', 'Завтрак')] + breakfast_choices
        day_form.lunch.choices = [('', 'Обед')] + lunch_choices
        day_form.dinner.choices = [('', 'Ужин')] + dinner_choices
        day_form.snack.choices = [('', 'Перекус')] + snack_choices
    
    return render_template(
        "menu/menu.html",
        form=form,
    )
