from . import bp
from flask import render_template
from app.blueprints.auth.models import User
from app.blueprints.dex.models import Pokemon

@bp.route('/id/<id>')
def poke_by_id(id):
    poke = Pokemon.query.get(id)
    return render_template('poke-by-id.html.j2', poke=poke)

@bp.route('/owner/<username>')
def pokes_by_owner(username):
    owner = User.query.filter_by(username=username).first()
    pokes = Pokemon.query.filter_by(owner_id=owner.id).all()
    return render_template('pokes-by-owner.html.j2', owner=owner, pokes=pokes)