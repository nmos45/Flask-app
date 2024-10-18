from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField,PasswordField,StringField,DecimalField,SelectField
from wtforms.validators import InputRequired, EqualTo

class PlatformChoice(FlaskForm):
    choice = RadioField(
        "Which platform?",
        choices=["Netflix","Amazon Prime","Disney"]
    )
    Country = SelectField(
        "Your Country",
        choices=[("ALL"), ("South Africa"), ("Canada"), ("Mexico"), ("India"),
                 ("France"), ("Japan"), ("Italy"), ("Romania"), ("Australia"),
                 ("United Kingdom"), ("United States")],
    )
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    user_id = StringField("User id:",validators=[InputRequired ()])
    password = PasswordField ("Password:",validators=[InputRequired()])
    password2 = PasswordField ("Repeat password:",validators=[InputRequired(), EqualTo("password" )])
    submit = SubmitField ("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:")
    password = PasswordField ("Password:")
    submit = SubmitField ("Submit")

class ReviewForm(FlaskForm):
    film = StringField("Film:",validators=[InputRequired ()])
    review = StringField("Review:",validators=[InputRequired ()])
    score = DecimalField("Score:",validators=[InputRequired ()])
    submit = SubmitField("Submit")

