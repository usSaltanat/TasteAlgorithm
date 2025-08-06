from wtforms import (
    Form,
    StringField,
    validators,
    PasswordField,
)


class SignUpForm(Form):
    login = StringField(
        "Логин",
        [
            validators.InputRequired(),
            validators.Length(min=3, max=50),
        ],
    )
    password = PasswordField(
        "Пароль",
        [
            validators.InputRequired(),
            validators.EqualTo('password_confirm', message="Пароли должны совпадать"),
            validators.Length(min=10, max=100),
            # TODO: 1) проверить что пароль надежный (содержит цифры, буквы, разный регистр, спец символы)
            # TODO: 2) пользовательское соглашение и согласие на обработку ПД
        ],
    )
    password_confirm = PasswordField(
        "Подтверждение пароля",
        [
            validators.InputRequired(),
        ]
    )
