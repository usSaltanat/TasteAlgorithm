from wtforms import Form, StringField, validators, SubmitField, SelectField


class ProductForm(Form):
    product_name = StringField(
        "Название продукта",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    product_category_id = SelectField(
        "Категория",
        [
            validators.InputRequired(),
            validators.NumberRange(
                min=1
            ),  # Проверяем, что ID категории положительное число
        ],
        coerce=int,
    )  # Преобразуем в целое число

    product_unit_id = SelectField(
        "Еденицы измерения",
        [
            validators.InputRequired(),
            validators.NumberRange(
                min=1
            ),  # Проверяем, что ID единицы измерения положительное число
        ],
        coerce=int,
    )  # Преобразуем в целое число

    submit = SubmitField("Сохранить")
