from wtforms import Form, StringField, validators, SelectField
from wtforms import SelectMultipleField


class MealForm(Form):
    name = StringField(
        "Название блюда",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    products = SelectMultipleField(
        "Список продуктов",
        coerce=int,
        validators=[validators.DataRequired()],
    )
    meals_category = SelectField(
        "Категория блюда",
        [
            validators.InputRequired(),
        ],
    )

    # recipe = StringField(
    #     "Рецепт",
    #     [
    #         validators.length(min=2, max=10),
    #         validators.DataRequired(),
    #     ],
    # )
