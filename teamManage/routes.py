from flask import render_template, url_for, redirect, flash
from teamManage import app
from teamManage.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		flash("Your account has been created!")
		return redirect(url_for("home"))
	return render_template("register.html",form=form)