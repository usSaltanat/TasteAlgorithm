import typing
import uuid
from functools import wraps

from flask import Blueprint, redirect, render_template, make_response, request, current_app, flash
from passlib.hash import pbkdf2_sha256

from forms.signin import LoginForm
from forms.signup import SignUpForm
from request_utils import get_session_from_cookies
from storage import Storage

bp = Blueprint('auth', __name__)


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        auth_session = get_session_from_cookies()
        if not auth_session:
            return redirect("/signin")
        kwargs["session"] = auth_session
        return view_func(*args, **kwargs)

    return wrapped_view


@bp.route("/signin", methods=["GET"])
def get_login():
    if get_session_from_cookies():
        return redirect("/")
    body = render_template("signin/signin.html", form=LoginForm())
    response = make_response(body)
    response.set_cookie("session_id", "", -1)
    return response


@bp.route("/signin", methods=["POST"])
def post_login():
    login = request.form["login"]
    password = request.form["password"]
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    user = storage.find_user_by_login(login)
    # print(f"❗️user = {user}")
    if user is not None:
        if pbkdf2_sha256.verify(password, user.password_hash):
            session_id = str(uuid.uuid4())
            storage.create_session(user, session_id)
            response = make_response("", 302)
            response.set_cookie("session_id", session_id, 60 * 60)
            response.headers["Location"] = "/"
            # print("❗️", response)
            return response
    flash("Неверное имя пользователя или пароль")
    return render_template("signin/signin.html", form=LoginForm())


@bp.route("/signup", methods=["GET"])
def get_signup():
    if get_session_from_cookies():
        return redirect("/")
    body = render_template("signup/signup.html", form=SignUpForm())
    response = make_response(body)
    response.set_cookie("session_id", "", -1)
    return response


@bp.route("/signup", methods=["POST"])
def post_signup():
    login = request.form["login"]
    password = request.form["password"]
    # хакер может при помощи Postman или curl отправить запрос со слабым паролем (даже пустым)
    storage = typing.cast(Storage, current_app.config["storage"])  # подключение к БД
    user = storage.find_user_by_login(login)
    if user is not None:
        flash("Логин занят, выберите другой")
        return render_template("signup/signup.html", form=SignUpForm())
    # зашифровать plaintext password
    password_hash = pbkdf2_sha256.hash(password)
    storage.signup(login, password_hash)
    return redirect("/")


@bp.route("/logout", methods=["GET"])
def get_logout():
    resp = make_response("", 302)
    resp.set_cookie("session_id", "", -1)
    resp.headers["Location"] = "/"
    return resp
