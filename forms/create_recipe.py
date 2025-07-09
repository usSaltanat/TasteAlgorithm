from wtforms import Form, StringField, validators, SubmitField, SelectField


class RecipeForm(Form):

    meal = SelectField(
        "Блюдо",
        [
            validators.InputRequired(),
        ],
    )

    recipe_body = StringField(
        "Рецепт",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )

    submit = SubmitField("Сохранить")
