from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from teamManage.models import User, Team

class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password")])
	gender = RadioField("Gender", choices=[("male","Male"),("female","Female")], validators=[DataRequired()])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username has been taken! Please choose another one!")

	def validate_email(self,email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError("Email has been taken! Please choose another one!")		


class TeamForm(FlaskForm):
	teamName = StringField("Team Name", validators=[DataRequired(), Length(min=2, max=50)])
	teamDescription = TextAreaField("Team Description", validators=[DataRequired()])
	teamMember = StringField("Members")
	submit = SubmitField("Create Team")



