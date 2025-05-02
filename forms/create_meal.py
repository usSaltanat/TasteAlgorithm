from wtforms import Form, StringField, validators, SubmitField, SelectField


class MealForm(Form):
    name = StringField(
        "Название блюда",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    meals_category = SelectField(
        "Категория блюда",
        [
            validators.InputRequired(),
        ],
    )
