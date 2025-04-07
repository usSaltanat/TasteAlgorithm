from wtforms import Form, StringField, validators, SubmitField


class MealsCategoryForm(Form):
    meals_category = StringField(
        "Новая категория блюда",
        [
            validators.Length(min=3, max=100),
            validators.DataRequired(),
        ],
    )
    submit = SubmitField("Сохранить")
