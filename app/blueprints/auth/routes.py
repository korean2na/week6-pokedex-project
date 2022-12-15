from . import bp
from app.blueprints.auth.models import User
from app import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

@bp.route('/login')
def login():
    return render_template('login.html.j2')

@bp.route('/login/email', methods=['POST'])
def login_email():
    email = request.form['email']
    password = request.form['password']
    next_url = request.form['next']

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash(f'An account with email "{email}" does not exist.', 'danger')

    elif user.check_my_password(password):
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        
        if next_url != '':
            return redirect(next_url)

        return redirect(url_for('main.home'))

    else:
        flash('Password was incorrect.', 'danger')

    return render_template('login.html.j2')

@bp.route('/login/username', methods=['POST'])
def login_username():
    username = request.form['username'].lower()
    password = request.form['password']
    next_url = request.form['next']

    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(f'An account with username "{username}" does not exist.', 'danger')

    elif user.check_my_password(password):
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        
        if next_url != '':
            return redirect(next_url)

        return redirect(url_for('main.home'))

    else:
        flash('Password was incorrect.', 'danger')

    return render_template('login.html.j2')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html.j2')

    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']
    username = request.form['username'].lower()
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    pw_hint = request.form['passHint']

    check_email = User.query.filter_by(email=email).first()
    check_username = User.query.filter_by(username=username).first()

    if check_email is not None:
        flash(f'An account with email address "{email}" already exists.', 'danger')

    elif check_username is not None:
        flash(f'An account with username "{username}" already exists.', 'danger')
    
    elif password != confirm_password:
        flash('Password and Confirm Password did not match.', 'danger')

    else:
        try:
            new_user = User(email=email, username=username, password='', first_name=first_name, last_name=last_name, pw_hint=pw_hint)
            new_user.hash_my_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account "{new_user.username}" created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('There was an error.', 'danger')

    return render_template('register.html.j2')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset-password.html.j2')

    curr_pass = request.form['currPass']
    new_pass = request.form['newPass']
    confirm_new = request.form['confirmNew']
    pass_hint = request.form['passHint']

    if not current_user.check_my_password(curr_pass):
        flash('Old password was incorrect.', 'danger')

    elif confirm_new != new_pass:
        flash('New Password and Confirm New Password did not match.', 'danger')

    else:
        current_user.hash_my_password(new_pass)
        current_user.pw_hint = pass_hint
        db.session.add(current_user)
        db.session.commit()
        flash('Password changed successfully!', 'success')

    return render_template('reset-password.html.j2')

@bp.route('/hint')
@login_required
def hint():
    return render_template('hint.html.j2')