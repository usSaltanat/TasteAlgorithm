from wtforms import Form, StringField, validators, SubmitField, SelectField


class ProductForm(Form):
    name = StringField(
        "Название продукта",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    category = SelectField(
        "Категория",
        [
            validators.InputRequired(),
        ],
    )

    unit = SelectField(
        "Единицы измерения",
        [
            validators.InputRequired(),
        ],
    )

    submit = SubmitField("Сохранить")
