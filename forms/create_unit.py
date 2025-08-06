from wtforms import Form, StringField, validators, SubmitField


class UnitForm(Form):
    unit = StringField(
        "Новая Единица измерения",
        [
            validators.length(min=2, max=10),
            validators.DataRequired(),
        ],
    )
    submit = SubmitField("Сохранить")
