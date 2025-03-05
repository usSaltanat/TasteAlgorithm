from wtforms import Form, StringField, validators, SubmitField


class CreateCategoryForm(Form):
    category = StringField(
        "Новая категория",
        [
            validators.Length(min=3, max=100),
            validators.DataRequired(),
        ],
    )
    submit = SubmitField("Сохранить")
