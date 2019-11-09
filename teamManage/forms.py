from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password")])
	gender = RadioField("Gender", choices=[("male","Male"),("female","Female")], validators=[DataRequired()])
	submit = SubmitField("Sign Up")

