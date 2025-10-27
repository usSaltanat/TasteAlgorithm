from wtforms import Form, StringField, validators, SubmitField, SelectField, FieldList, FormField


class DailyMenuForm(Form):
    breakfast = SelectField(
        "",
        [
            validators.InputRequired(),
        ],
    )

    lunch = SelectField(
        "",
        [
            validators.InputRequired(),
        ],
    )

    dinner = SelectField(
        "",
        [
            validators.InputRequired(),
        ],
    )

    snack = SelectField(
        "",
        [
            validators.InputRequired(),
        ],
    )


class WeeklyMenuForm(Form):
    days = FieldList(FormField(DailyMenuForm), min_entries=7)

    # submit = SubmitField("Сохранить")
