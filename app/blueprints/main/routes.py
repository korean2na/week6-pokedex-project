from . import bp
from flask import render_template
from flask_login import login_required

@bp.route('/')
@login_required
def home():
    return render_template('home.html.j2')

@bp.route('/about')
def about():
    return render_template('about.html.j2')