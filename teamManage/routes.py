import os
import secrets
from flask import render_template, url_for, redirect, flash, request, abort
from teamManage import app, db, bcrypt, socketio
from PIL import Image

from teamManage.forms import RegisterForm, LoginForm, TeamForm, AddMemberForm, TaskForm, UpdateProfileForm, \
EditTaskForm, PostForm,CommentForm, EditTeamForm
from teamManage.models import User, Team, Task,Post,Comment
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime, timedelta
from flask_socketio import send, emit, join_room, leave_room
import json


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Team Manager")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                    password=pw_hash, gender=form.gender.data, phoneNumber=form.phoneNumber.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("team"))
        else:
            flash("Login unsucessful! Please check your email and password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", title="Login", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def remove_picture(user_picture):
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', user_picture)
    os.remove(picture_path)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return redirect(url_for('other_profile', user_id=current_user.id))


@app.route('/profile/<int:user_id>', methods=['GET'])
def other_profile(user_id):
    form = UpdateProfileForm()
    user = User.query.get_or_404(user_id)
    profile_image = url_for(
        'static', filename='profile_pics/' + user.profile_image)
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
    profile_image = url_for(
        'static', filename='profile_pics/' + user.profile_image)
    return render_template('profile.html', title='Profile Page', profile_image=profile_image, user=user, form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logout", "primary")
    return redirect(url_for("home"))


@app.route("/team")
@login_required
def team():
    teams = Team.query.filter(Team.members.any(
        username=current_user.username)).all()
    team_data = []
    i = 0
    for team in teams:
        progress = 0
        team_data.append({})
        team_data[i]["id"] = team.id
        team_data[i]["name"] = team.name
        team_data[i]["description"] = team.description
        team_data[i]["members"] = len(team.members.all())
        team_data[i]["tasks"] = len(team.tasks)
        for index in range(len(team.tasks)):
            if team.tasks[index].status == True:
                progress += 1
        if len(team.tasks) == 0:
            team_data[i]["progress"] = "100"
        else:
            team_data[i]["progress"] = str(progress / len(team.tasks) * 100)
        i += 1
    return render_template("team.html", title="Your team", teams=teams, team_data=team_data)


@app.route("/team/<int:team_id>", methods=["GET", "POST", "PUT"])
def myTeam(team_id):
	team = Team.query.get_or_404(team_id)
	if current_user not in team.members.all():
		return (abort(403))

	form_edit_team = EditTeamForm()
	form_add_member = AddMemberForm()
	form_add_task = TaskForm()
	form_edit_task = EditTaskForm()
	tasks = team.tasks
	members = team.members
	time = datetime.utcnow()
	progress = 0 
	member_data = []
	task_data = []
	totalTaskComplete = 0
	#Task Processing
	i = 0
	for task in tasks:
		task_data.append({})
		create_in = datetime.utcnow() - task.date_created
	
		if task.status == True:
			complete_in = datetime.utcnow() - task.date_completed
			totalTaskComplete += 1
			progress += 1
			task_data[i]["date_completed_day"] = int(round(divmod(complete_in.days * 86400 + complete_in.seconds, 60)[0] / 1440))
			task_data[i]["date_completed_hour"] = int(round(divmod(complete_in.days * 86400 + complete_in.seconds, 60)[0] / 60))
			task_data[i]["date_completed_minute"] = divmod(complete_in.days * 86400 + complete_in.seconds, 60)[0]
			task_data[i]["date_completed_second"] = divmod(complete_in.days * 86400 + complete_in.seconds, 60)[1]
			task_data[i]["complete_by"] = []
			task_data[i]["user_image"] = []
			for user in task.completeBy.all():
				task_data[i]["complete_by"].append(user.username)
				task_data[i]["user_image"].append(user.profile_image)


		task_data[i]["id"] = task.id
		task_data[i]["name"] = task.name
		task_data[i]["status"] = task.status
		task_data[i]["description"] = task.description
		task_data[i]["date_created_day"] = int(round(divmod(create_in.days * 86400 + create_in.seconds, 60)[0] / 1440))
		task_data[i]["date_created_hour"] = int(round(divmod(create_in.days * 86400 + create_in.seconds, 60)[0] / 60))
		task_data[i]["date_created_minute"] = divmod(create_in.days * 86400 + create_in.seconds, 60)[0]
		task_data[i]["date_created_second"] = divmod(create_in.days * 86400 + create_in.seconds, 60)[1]

		i += 1
	if len(tasks) == 0:
		progress = 100
	else:
		progress = round(progress / len(tasks) * 100)
	
	i = 0 #index in member_data
	#Member Contribution
	for member in members:
		member_data.append({})
		member_data[i]['name'] = member.username
		taskDone = 0
		for task in tasks:
			if task.completeBy:
				for user in task.completeBy.all():
					if user.username == member.username: #Need to work on after changing the database
						taskDone += 1
		member_data[i]['taskDone'] = taskDone #Definitely need to check 
		i += 1

	#Separate 2 form validation
	if form_add_member.submit_member.data and form_add_member.validate_on_submit():
		member_in_team = []
		membersAdd = form_add_member.teamMembers.data.split(', ')

		for member in team.members.all(): #find all the member of the team	
			member_in_team.append(member.username)

		for member in membersAdd: 
			if not (member in member_in_team): # a condition to check if member is already in the team or not
				user = User.query.filter_by(username=member).first() # those line will ensure that the DB wont have any duplicated rows
				team.members.append(user)
			else:
				flash("%s is already in your team" %(member), "info" )
		db.session.commit()

	if form_add_task.submit_task.data and form_add_task.validate_on_submit():
		task = Task(name=form_add_task.name.data, description=form_add_task.description.data, inTeam=team)
		db.session.add(task)
		db.session.commit()

	if form_edit_team.submit.data and form_edit_team.validate():
		team.name = form_edit_team.teamName.data
		db.session.commit()

	if request.method == 'POST':
		if request.form.get('editId'):
			task = Task.query.get(request.form.get('editId'))
			task.name = request.form.get('editName')
			task.description = request.form.get('editDescription')
			db.session.commit()
		if request.form.get('completeId'):
			task = Task.query.get(request.form.get('completeId'))
			task.status = True
			task.date_completed = datetime.utcnow()
			membersComplete = request.form.getlist('membersComplete')
			for member in membersComplete:
				user = User.query.filter_by(username=member).first()
				task.completeBy.append(user)
				db.session.commit()
	

	return render_template(
		"myteam.html", 
		title=team.name, 
		team=team, 
		form_edit_team=form_edit_team,
		form_add_member=form_add_member, 
		form_add_task=form_add_task,
		form_edit_task=form_edit_task,
		progress=progress,
		member_data=member_data,
		totalTaskComplete=totalTaskComplete,
		task_data=task_data
		)	



# -----------------------------TASK ROUTE -----------------------------


@app.route("/team/<int:team_id>/<int:task_id>/complete", methods=["GET", "POST"])
def completeTask(team_id, task_id):
    task = Task.query.get_or_404(task_id)
    task.status = True
    task.completeBy.append(current_user)
    task.date_completed = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("myTeam", team_id=task.inTeam.id))


@app.route("/team/<int:team_id>/<int:task_id>/delete", methods=["GET", "POST"])
def deleteTask(team_id, task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('myTeam', team_id=team_id))


# --------------------------------------------------------------------------------------
@app.route("/team/create", methods=["GET", "POST"])
@login_required
def create_team():
    form = TeamForm()
    if form.validate_on_submit():
        members = form.teamMembers.data.split(', ')
        team = Team(name=form.teamName.data,
                    description=form.teamDescription.data, teamLeader=current_user)
        db.session.add(team)
        for member in members:  # looping in the adding member field
            if member == '':
                team.members.append(current_user)
            else:
                team.members.append(current_user)
                newMember = User.query.filter_by(username=member).first()
                team.members.append(newMember)
        db.session.commit()
        flash("Your team has been created!", "success")
        # later will redirect to team/team_id url team_id
        return redirect(url_for("myTeam", team_id=team.id))
    return render_template("create_team.html", form=form, title="Team Create")


@app.route("/team/<int:team_id>/edit", methods=["GET", "POST"])
def edit_team(team_id):
	form = EditTeamForm()
	team = Team.query.get_or_404(team_id)
	
	return redirect(url_for("myTeam",team_id=team.id)) 



@app.route("/team/<int:team_id>/delete", methods=["GET", "POST"])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    if team.teamLeader == current_user:
        for member in team.members.all():
            team.members.remove(member)
        for task in team.tasks:
            db.session.delete(task)
        db.session.delete(team)
        db.session.commit()
        return redirect(url_for("team"))

    else:
        flash('You are not the team leader', 'danger')
        return redirect(url_for("myTeam", team_id=team.id))


@app.route("/team/<int:team_id>/leave", methods=["GET", "POST"])
def leave_team(team_id):
    team = Team.query.get_or_404(team_id)
    if current_user in team.members.all():
        team.members.remove(current_user)
        if team.teamLeader.username == current_user.username:
            if len(team.members.all()) > 0:
                team.teamLeader = team.members[0]
        db.session.commit()
        return redirect(url_for("team"))



@app.route("/team/<int:team_id>/remove/<int:member_id>", methods=["GET", "POST"])
def remove_member(team_id, member_id):
    team = Team.query.get_or_404(team_id)
    if current_user == team.teamLeader:
        member = User.query.filter_by(id=member_id).first()
        team.members.remove(member)
        db.session.commit()
    else:
        flash('You are not the team leader', 'danger')
    return redirect(url_for("myTeam", team_id=team.id))


@app.route('/chat', methods=["GET", "POST"])
@login_required
def sessions():
	team = Team.query.get_or_404(request.args.get('team_id'))
	if current_user not in team.members.all():
		return (abort(403))
	return render_template('chat.html')



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    print('message was received!!!')
    print('message was received!!!')






@socketio.on('join', namespace='/chat')
def join(room):
    join_room(int(room))
    print("Room number:", room)
    print(current_user.username + ' has entered the room. ', room)
    send(current_user.username + ' has joined', room=room)


@socketio.on('my event', namespace='/chat')
def handle_custom_event(json, methods=['GET','POST']):
	team_id = request.args.get('team_id')
	
	while team_id == None:
		team_id = request.args.get('team_id')
	print("message received:" + str(json))
	emit('my response', json, callback=messageReceived(), room=int(team_id))


@app.route('/team/<int:team_id>/discussion/new', methods=['GET','POST'])
@login_required
def discussion(team_id):
	team = Team.query.get_or_404(team_id)
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user,location = team)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('discussion_list',team_id=team.id))
	return render_template('discussion.html', title='New Post',
						   form=form, legend='New Post')

@app.route('/team/<int:team_id>/discussion', methods=['GET','POST'])
@login_required
def discussion_list(team_id):
	team = Team.query.get_or_404(team_id)
	posts = Post.query.filter_by(location=team)
	return render_template('discussion_list.html', posts=posts,team=team)

@app.route('/team/<int:team_id>/discussion/<int:post_id>', methods=['GET','POST'])
@login_required
def post(team_id,post_id):
	team = Team.query.get_or_404(team_id)
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter_by(article=post)
	return render_template('post.html', title=post.title, post=post,team=team,comments=comments)

@app.route('/team/<int:team_id>/discussion/<int:post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(team_id,post_id):
	with db.session.no_autoflush:
		team = Team.query.get_or_404(team_id)
		post = Post.query.get_or_404(post_id)
		if post.author != current_user:
			flash('You can not delete this post !', 'danger')
			return redirect(url_for('discussion_list', team_id=team.id))

		db.session.delete(post)
		for comment in post.comment:
			db.session.delete(comment)
		db.session.commit()
		flash('Your post has been deleted!', 'success')
		return redirect(url_for('discussion_list', team_id=team.id))


@app.route('/team/<int:team_id>/discussion/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id,team_id):
	team = Team.query.get_or_404(team_id)
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		flash('You can not update this post !', 'danger')
		return redirect(url_for('discussion_list', team_id=team.id))
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('discussion_list',team_id=team.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('discussion.html', title='Update Post',
						   form=form, legend='Update Post')

@app.route('/team/<int:team_id>/discussion/<int:post_id>/addcomment', methods=['GET','POST'])
@login_required
def add_comment(post_id,team_id):
	team = Team.query.get_or_404(team_id)
	post = Post.query.get_or_404(post_id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(content=form.content.data,article = post, user = current_user)
		db.session.add(comment)
		db.session.commit()
		flash('Your comment has been created!', 'success')
		return redirect(url_for('post', team_id=team.id,post_id=post.id))
	return render_template('new_comment.html',form=form, legend='Add comment')

@app.route('/team/<int:team_id>/discussion/<int:post_id>/comment/<int:comment_id>/delete', methods=['GET','POST'])
@login_required
def delete_comment(post_id,team_id,comment_id):
	team = Team.query.get_or_404(team_id)
	post = Post.query.get_or_404(post_id)
	comment = Comment.query.get_or_404(comment_id)
	if post.author == current_user or comment.user == current_user:
		db.session.delete(comment)
		db.session.commit()
	else:
		flash('You can not delete this comment !', 'danger')
		return redirect(url_for('post', team_id=team.id,post_id=post.id))

	return redirect(url_for('post', team_id=team.id,post_id=post.id))

@app.route('/team/<int:team_id>/discussion/<int:post_id>/comment/<int:comment_id>/update', methods=['GET','POST'])
@login_required
def update_comment(post_id,team_id,comment_id):
	comment = Comment.query.get_or_404(comment_id)
	team = Team.query.get_or_404(team_id)
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		flash('You can not update this comment !', 'danger')
		return redirect(url_for('post', team_id=team.id,post_id=post.id))
	form = CommentForm()
	if form.validate_on_submit():
		comment.content = form.content.data
		db.session.commit()
		flash('Your comment has been updated!', 'success')
		return redirect(url_for('post',team_id=team.id,post_id=post.id))
	elif request.method == 'GET':
		form.content.data = comment.content
	return render_template('new_comment.html', title='Update comment',
						   form=form, legend='Update comment')


@socketio.on('my event', namespace='/chat')
def handle_custom_event(json, methods=['GET', 'POST']):
    team_id = request.args.get('team_id')
    while team_id == None:
        team_id = request.args.get('team_id')
    print("message received:" + str(json))
    emit('my response', json, callback=messageReceived(), room=int(team_id))
