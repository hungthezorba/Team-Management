from flask import render_template, url_for, redirect, flash, request
from teamManage import app, db, bcrypt
from teamManage.forms import RegisterForm, LoginForm, TeamForm, AddMemberForm, TaskForm, UpdateProfileForm
from teamManage.models import User, Team, Task
from flask_login import login_user, current_user, login_required, logout_user

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html", title="Team Manager")

@app.route("/register", methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RegisterForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password=pw_hash, gender=form.gender.data, phoneNumber=form.phoneNumber.data)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created!")
		return redirect(url_for("home"))
	return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash("Login successful!")
			return redirect(url_for("home"))
		else:
			flash("Login unsucessful! Please check your email and password")
			return redirect(url_for("login"))
	return render_template("login2.html", title="Login", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def remove_picture(user_picture):
    picture_path = os.path.join(app.root_path, 'static/profile_pics', user_picture)
    os.remove(picture_path)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
   return redirect(url_for('other_profile', user_id=current_user.id))




@app.route('/profile/<int:user_id>', methods=['GET'])
def other_profile(user_id):
    form = UpdateProfileForm()
    user = User.query.get_or_404(user_id)
    profile_image = url_for('static', filename='profile_pics/' + user.profile_image)
    return render_template('profile.html', title='Profile Page', profile_image=profile_image, user=user, form=form)

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.profile_image.data:
            if current_user.profile_image == 'default.jpg':
                picture_file = save_picture(form.profile_image.data)
                current_user.profile_image = picture_file
            else:
                remove_picture(current_user.profile_image)
                picture_file = save_picture(form.profile_image.data)
                current_user.profile_image = picture_file
        current_user.username = form.username.data
        current_user.phoneNumber = form.phoneNumber.data
        current_user.gender = form.gender.data
        current_user.biography = form.biography.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.phoneNumber.data = current_user.phoneNumber
        form.gender.data = current_user.gender
        form.biography.data = current_user.biography
    profile_image = url_for('static', filename='profile_pics/' + user.profile_image)
    return render_template('profile.html', title='Profile Page', profile_image=profile_image, user=user, form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/team")
@login_required
def team():
	teams = Team.query.all()
	return render_template("team.html", title="Your team", teams=teams)


@app.route("/team/<int:team_id>", methods=["GET","POST"])
def myTeam(team_id):
	team = Team.query.get_or_404(team_id)
	form_add_member = AddMemberForm()
	form_add_task = TaskForm()
	form_update_task = TaskForm()

	#Separate 2 form validation
	if form_add_member.submit_member.data and form_add_member.validate(): 
		members = form_add_member.teamMembers.data.split(', ')
		for member in members:
			user = User.query.filter_by(username=member).first()
			team.members.append(user)
		db.session.commit()

	if form_add_task.submit_task.data and form_add_task.validate():
		task = Task(name=form_add_task.name.data, description=form_add_task.description.data, inTeam=team)
		db.session.add(task)
		db.session.commit()

	return render_template(
		"team_manage.html", 
		title=team.name, 
		team=team, 
		form_add_member=form_add_member, 
		form_add_task=form_add_task,
		form_update_task=form_update_task
		)	


@app.route("/team/<int:team_id>/<int:task_id>", methods=["GET", "POST"])
def updateTask(team_id,task_id):
	task = Task.query.get_or_404(task_id)
	form_update_task = TaskForm()
	if form_update_task.validate_on_submit():
		task.name = form_update_task.name.data
		task.description = form_update_task.description.data
		task.status = form_update_task.status.data
		db.session.commit()
	form_update_task.name.data	= task.name
	form_update_task.description.data = task.description
	form_update_task.status.data = task.status
	return render_template("task.html", title=task.name, task=task, form_update_task=form_update_task)

@app.route("/team/<int:team_id>/<int:task_id>/complete", methods=["GET", "POST"])
def completeTask(team_id,task_id):
	task = Task.query.get_or_404(task_id)
	task.status = True
	db.session.commit()
	return redirect(url_for("myTeam",team_id=task.inTeam.id))


@app.route("/team/create", methods=["GET","POST"])
@login_required
def create_team():
	form = TeamForm()
	if form.validate_on_submit():
		members = form.teamMembers.data.split(', ')
		team = Team(name=form.teamName.data, description=form.teamDescription.data)
		db.session.add(team)
		team.members.append(current_user)
		db.session.commit()
		flash("Your team has been created!")
		return redirect(url_for("myTeam",team_id=team.id)) # later will redirect to team/team_id url team_id
	return render_template("create_team.html",form=form, title="Team Create")

