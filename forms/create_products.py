from wtforms import Form, StringField, validators, SubmitField


class ProductForm(Form):
    product = StringField(
        "Название продукта",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    submit = SubmitField("Сохранить")
