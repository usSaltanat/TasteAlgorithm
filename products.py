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
from forms.create_product import ProductForm
from storage import Storage
from storage_entities import Session, Product, Category, Unit, User

bp = Blueprint("products", __name__)


@bp.route("/products", methods=["GET"])
@login_required
def get_products_route(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    # print(f"❗️user = {user}")
    view = storage.get_products(session.user)
    return render_template("products/products.html", products=view)


@bp.route("/products/<int:id>", methods=["GET"])
@login_required
def get_product_by_id_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id, session.user)
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template("products/product.html", product=product_view)


# Создание продукта
@bp.route("/products/new", methods=["GET"])
@login_required
def new_product(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    form = ProductForm()
    form.category.choices = [
        (category.id, category.name)
        for category in storage.get_categories(session.user)
    ]
    form.unit.choices = [
        (unit.id, unit.name) for unit in storage.get_units(session.user)
    ]
    return render_template(
        "products/new.html",
        form=form,
    )


@bp.route("/products/create", methods=["POST"])
@login_required
def create_product(session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_to_create = Product(
        None,
        request.form["name"],
        Category(int(request.form["category"]), None, None),
        Unit(int(request.form["unit"]), None, None),
        User(int(session.user.id), None, None),
    )
    # print("❗️", product_to_create)
    created_product_id = storage.insert_product(product_to_create)
    if created_product_id is None:
        flash("Не удалось создать продукт")
        form = ProductForm()
        form.category.choices = [
            (category.id, category.name)
            for category in storage.get_categories(session.user)
        ]
        form.unit.choices = [
            (unit.id, unit.name) for unit in storage.get_units(session.user)
        ]
        return render_template(
            "products/new.html",
            form=form,
        )
    return redirect(f"/products/{created_product_id}")


@bp.route("/products/<int:id>/delete", methods=["GET"])
@login_required
def delete_product_by_id_route(id: str, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    deleted_product_id = storage.delete_product_by_id(id, session.user)
    if deleted_product_id is None:
        flash("Не удалось удалить продукт")
    return redirect(f"/products")


@bp.route("/products/<int:id>/edit", methods=["GET"])
@login_required
def edit_product_by_id(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id, session.user)
    form = ProductForm()
    form.name.data = product_view.name
    form.category.choices = [
        (category.id, category.name)
        for category in storage.get_categories(session.user)
    ]
    form.unit.choices = [
        (unit.id, unit.name) for unit in storage.get_units(session.user)
    ]
    if product_view is None:
        return abort(404, "Продукт не найден")
    return render_template(
        "products/edit.html",
        product=product_view,
        form=form,
    )


@bp.route("/products/<int:id>/update", methods=["POST"])
@login_required
def update_product_route(id: int, session: Session):
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    product_view = storage.get_product_by_id(id, session.user)
    product_to_update = Product(
        id,
        request.form["name"],
        Category(int(request.form["category"]), None, None),
        Unit(int(request.form["unit"]), None, None),
        User(int(session.user.id), None, None),
    )
    updated_product_id = storage.update_product(product_to_update)
    if updated_product_id is None:
        flash("Не удалось изменить продукт")
        product_view = storage.get_product_by_id(id, session.user)
        form = ProductForm()
        form.category.choices = [
            (category.id, category.name)
            for category in storage.get_categories(session.user)
        ]
        form.unit.choices = [
            (unit.id, unit.name) for unit in storage.get_units(session.user)
        ]
        return render_template(
            "products/edit.html",
            product=product_view,
            form=form,
        )
    return redirect(f"/products/{updated_product_id}")
