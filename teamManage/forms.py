from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from teamManage.models import User, Team
from flask_login import current_user
from wtforms.widgets import html5

class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password")])
	gender = RadioField("Gender", choices=[("male","Male"),("female","Female")], validators=[DataRequired()])
	phoneNumber = IntegerField("Phone Number", validators=[DataRequired()])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username has been taken! Please choose another one!")

	def validate_email(self,email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError("Email has been taken! Please choose another one!")		

	def validate_phoneNumber(self,phoneNumber):
		phoneNumber = User.query.filter_by(phoneNumber=phoneNumber.data).first()
		if phoneNumber:
			raise ValidationError("Phone number has been taken! Please choose another one!")	

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")



class TeamForm(FlaskForm):
	teamName = StringField("Team Name", validators=[DataRequired(), Length(min=2, max=50)])
	teamDescription = TextAreaField("Team Description", validators=[DataRequired()])
	teamMembers = StringField("Members")
	submit = SubmitField("Create Team")

	def validate_teamMembers(self, teamMembers):
		if teamMembers.data != '':
			members = teamMembers.data.split(', ')
			for member in members:
				user = User.query.filter_by(username=member).first()
				if user:
					pass
				else:
					raise ValidationError("%s is not a Team Manager's member" %(member))
		
class AddMemberForm(FlaskForm):
	teamMembers = StringField("Members",validators=[DataRequired()])
	submit_member = SubmitField("Add")

	def validate_teamMembers(self, teamMembers):
		members = teamMembers.data.split(', ')
		for member in members:
			user = User.query.filter_by(username=member).first()
			if user:
				pass
			else:
				raise ValidationError("%s is not a Team Manager's member" %(member))
	
		

class TaskForm(FlaskForm):
	name = StringField("Task Name", validators=[DataRequired()])
	description = TextAreaField("Task Description")
	status = BooleanField("Status")
	submit_task = SubmitField("Add Task")

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phoneNumber = StringField('Phone Number',validators=[Length(min=0, max=15)], widget=html5.NumberInput())
    gender = StringField('Gender', validators=[DataRequired()])
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    biography = TextAreaField('Your Biography:', validators=[Length(min=0, max=160)])
    submit = SubmitField('Update!')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    def validate_phone(self, phoneNumber):
        if phoneNumber.data != current_user.phoneNumber:
            phone = User.query.filter_by(phoneNumber=phoneNumber.data).first()
            if phone:
                raise ValidationError('That phone number is already claimed. Please choose a different one.')




