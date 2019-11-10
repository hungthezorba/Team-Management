from flask import render_template, url_for, redirect, flash
from teamManage import app, db, bcrypt
from teamManage.forms import RegisterForm, TeamForm
from teamManage.models import User, Team

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html", title="Team Manager")

@app.route("/register", methods=["GET","POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password=pw_hash, gender=form.gender.data)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created!")
		return redirect(url_for("home"))
	return render_template("register.html",form=form, title="Register")

@app.route("/team/<team_id>")
def team(team_id):
	return "hello"


@app.route("/team/create", methods=["GET","POST"])
def create_team():
	form = TeamForm()
	if form.validate_on_submit():
		members = form.teamMember.data.split(', ')
		team = Team(teamName=form.teamName.data, teamDescription=form.teamDescription.data)
		db.session.add(team)
		for member in members:
			user = User.query.filter_by(username=member).first()
			team.member.append(user)
		db.session.commit()
		flash("Your team has been created!")
		return redirect(url_for("home")) # later will redirect to team/team_id url team_id
	return render_template("create_team.html",form=form, title="Team Create")

