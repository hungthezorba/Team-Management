import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
    if user:
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        flash('Login Successfully.', 'success')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
        flash('Please try again. Check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    user = current_user
    profile_image = url_for('static', filename='profile_pics/' + user.profile_image)
    return render_template('profile.html', title='Profile Page', profile_image=profile_image, user=user)

@app.route('/profile/<int:user_id>')
def other_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile_image = url_for('static', filename='profile_pics/' + user.profile_image)
    return render_template('profile.html', title='Profile Page', profile_image=profile_image, user=user)




