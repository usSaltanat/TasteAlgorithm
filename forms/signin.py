from wtforms import (
    Form,
    StringField,
    validators,
    PasswordField,
)


class LoginForm(Form):
    login = StringField(
        "Логин",
        [
            validators.InputRequired(),
        ],
    )
    password = PasswordField(
        "Пароль",
        [
            validators.InputRequired(),
        ],
    )
