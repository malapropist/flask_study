from flask import Blueprint, render_template, request, flash

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

        if len(email) < 4:
            flash('Email must be longer than 4 char', category='error')
            flash('good job nerd', category='success')
        elif len(fname) <2:
            flash('fname must be longer than 1 char', category='error')
        elif p1 != p2:
            flash('pwds dfon\'t match', category='error')
        else:
            # add user to database
            flash('good job nerd', category='success')

    return render_template("sign_up.html")