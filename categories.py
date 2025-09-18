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
from forms.create_category import CategoryForm
from storage import Storage
from storage_entities import Session, Category

bp = Blueprint("categories", __name__)


@bp.route("/categories", methods=["GET"])
@login_required
def get_categories_route(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_categories(session.user)
    return render_template("categories/categories.html", categories=view)


@bp.route("/categories/<int:id>", methods=["GET"])
@login_required
def get_category_by_id_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    category_view = storage.get_category_by_id(id, session.user)
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template("categories/category.html", category=category_view)


@bp.route("/categories/new", methods=["GET"])
@login_required
def new_category(session: Session):
    form = CategoryForm()
    return render_template("categories/new_category.html", form=form)


@bp.route("/categories/create", methods=["POST"])
@login_required
def create_category(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    if not form.validate():
        return render_template("categories/new_category.html", form=form)
    category_to_create = Category(None, form.category.data, session.user)
    created_category_id = storage.insert_category(category_to_create)
    if created_category_id is None:
        flash("Не удалось создать категорию")
        return render_template("categories/new_category.html", form=form)
    return redirect(f"/categories/{created_category_id}")


@bp.route("/categories/<int:id>/delete", methods=["GET"])
@login_required
def delete_category_by_id_route(id: str, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_category_id = storage.delete_category_by_id(id, session.user)
    if deleted_category_id is None:
        flash("Не удалось удалить категорию")
        # return redirect(f"/categories/{id}")
    return redirect(f"/categories")


@bp.route("/categories/<int:id>/edit", methods=["GET"])
@login_required
def edit_category_by_id(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    category_view = storage.get_category_by_id(id, session.user)
    form = CategoryForm()
    form.category.data = category_view.name
    if category_view is None:
        return abort(404, "Категория не найдена")
    return render_template(
        "categories/edit_category.html", category=category_view, form=form
    )


@bp.route("/categories/<int:id>/update", methods=["POST"])
@login_required
def update_category_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = CategoryForm(request.form)
    category_view = storage.get_category_by_id(id, session.user)
    if not form.validate():
        return render_template(
            "categories/edit_category.html", category=category_view, form=form
        )
    category_to_update = Category(id, form.category.data, session.user)
    updated_category_id = storage.update_category(category_to_update)
    if updated_category_id is None:  # обход случая когда категории повторяются
        flash("Не удалось изменить категорию")
        return render_template(
            "categories/edit_category.html", category=category_view, form=form
        )
    return redirect(f"/categories/{updated_category_id}")
