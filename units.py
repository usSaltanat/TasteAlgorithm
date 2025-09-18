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
from forms.create_unit import UnitForm
from storage import Storage
from storage_entities import Session, Unit

bp = Blueprint("units", __name__)


@bp.route("/units", methods=["GET"])
@login_required
def get_units_route(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    view = storage.get_units(session.user)
    return render_template("units/units.html", units=view)


@bp.route("/units/new", methods=["GET"])
@login_required
def new_unit(session: Session):
    form = UnitForm()
    return render_template("units/new_unit.html", form=form)


@bp.route("/units/create", methods=["POST"])
@login_required
def create_unit(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = UnitForm(request.form)
    if not form.validate():
        return render_template("units/new_unit.html", form=form)
    unit_to_create = Unit(None, form.unit.data, session.user)
    created_unit_id = storage.insert_unit(unit_to_create)
    if created_unit_id is None:
        flash("Не удалось создать еденицу измерения")
        return render_template("units/new_unit.html", form=form)
    return redirect(f"/units/{created_unit_id}")


@bp.route("/units/<int:id>", methods=["GET"])
@login_required
def get_unit_by_id_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id, session.user)
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template("units/unit.html", unit=unit_view)


@bp.route("/units/<int:id>/delete", methods=["GET"])
@login_required
def delete_unit_by_id_route(id: str, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_unit_id = storage.delete_unit_by_id(id, session.user)
    if deleted_unit_id is None:
        flash("Не удалось удалить еденицу измерения")
    return redirect(f"/units")


@bp.route("/units/<int:id>/edit", methods=["GET"])
@login_required
def edit_unit_by_id(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id, session.user)
    form = UnitForm(request.form)
    form.name.data = unit_view.name
    if unit_view is None:
        return abort(404, "Единица измерения не найдена")
    return render_template(
        "units/edit_unit.html",
        unit=unit_view,
        form=form,
    )


@bp.route("/units/<int:id>/update", methods=["POST"])
@login_required
def update_unit_route(id: int, session: Session):
    form = UnitForm(request.form)
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    unit_view = storage.get_unit_by_id(id, session.user)
    if not form.validate():
        return render_template("units/edit_unit.html", unit=unit_view, form=form)
    unit_to_update = Unit(
        id,
        form.unit.data,
        session.user,
    )
    updated_unit_id = storage.update_unit(unit_to_update)
    if updated_unit_id is None:
        flash("Не удалось изменить еденицу измерения")
        return render_template("units/edit_unit.html", unit=unit_view, form=form)
    return redirect(f"/units/{updated_unit_id}")
