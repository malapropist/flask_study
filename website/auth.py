from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    print(email)
    password = request.form.get('password')
    print(password)
    return render_template("login.html", boolean="Swagmoneys")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        p1 = request.form.get('password1')
        p2 = request.form.get('password2')
        if User.query.filter_by(email=email).first():
            print(User.query.filter_by(email=email).first().email)
            flash('Email is already used.')
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

    return render_template("sign_up.html")