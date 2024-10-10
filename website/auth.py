from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Incorrect email.', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        p1 = request.form.get('password1')
        p2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash(f'\'{user.email}\' is already used.')
        elif len(email) < 1:
            flash('Email must be longer than 4 char', category='error')
            flash('good job nerd', category='success')
        elif len(fname) <1:
            flash('fname must be longer than 1 char', category='error')
        elif p1 != p2:
            flash('pwds dfon\'t match', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=fname, password=generate_password_hash(
                p1, method='pbkdf2:sha256:600000'))
            db.session.add(new_user)
            db.session.commit()
            flash('good job nerd', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)