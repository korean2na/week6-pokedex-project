from . import bp
from app import db
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.auth.models import User
from app.blueprints.dex.models import Pokemon
from flask_login import current_user, login_required
import requests

def id_filter(x):
    return x.id

def name_filter(x):
    return x.name

def nick_filter(x):
    return x.nickname

@bp.route('/pokemon')
def pokemon():
    pokes = Pokemon.query.all()
    pokes.sort(key=id_filter)
    return render_template('pokemon.html.j2', pokes=pokes)

@bp.route('/pokemon/available')
@login_required
def available():
    pokes = Pokemon.query.filter_by(owner_id=None).all()
    pokes.sort(key=id_filter)
    return render_template('available.html.j2', pokes=pokes)

@bp.route('/collection')
@login_required
def collection():
    pokes = Pokemon.query.filter_by(owner_id=current_user.id).all()
    pokes.sort(key=nick_filter)
    pokes.sort(key=name_filter)
    return render_template('collection.html.j2', pokes=pokes)

@bp.route('/new_pokemon', methods=['GET', 'POST'])
def new_pokemon():
    if request.method == 'GET':
        return render_template('new-pokemon.html.j2')

    name = request.form['name'].lower()
    nickname = request.form['nickname']
    description = request.form['description']

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')

    if response.status_code == 200:
        data = response.json()

    else:
        flash(f'Oops! Looks like "{name}" is not a valid Pokémon. Please try again.', 'danger')
        return render_template('new-pokemon.html.j2')

    poke_num = data['id']
    type1 = data['types'][0]['type']['name']
    if len(data['types']) == 2:
        type2 = data['types'][1]['type']['name']

    else:
        type2 = None
    sprite = data['sprites']['front_default']

    new_poke = Pokemon(name=name, poke_num=poke_num, type1=type1, type2=type2, sprite=sprite, nickname=nickname, description=description, owner_id=None)
    db.session.add(new_poke)
    db.session.commit()
    if nickname == '':
        flash(f'{name.title()} added successfully!', 'success')

    else:
        flash(f'{nickname} added successfully!', 'success')

    return redirect(url_for('dex.pokemon'))

@bp.route('/collect', methods=['POST'])
@login_required
def collect():
    id = request.form['collectID']
    caught = Pokemon.query.filter_by(id=id).first()
    if caught.owner_id == None:
        caught.owner_id = current_user.id
        db.session.commit()
        if caught.nickname == '':
            flash(f'{caught.name.title()} collected successfully!', 'success')

        else:
            flash(f'{caught.nickname} collected successfully!', 'success')

    else:
        flash(f'Oops! Looks like that Pokémon already has an owner.', 'danger')
        return redirect(url_for('dex.available'))

    return redirect(url_for('dex.collection'))

@bp.route('/release', methods=['POST'])
@login_required
def release():
    id = request.form['releaseID']
    released = Pokemon.query.filter_by(id=id).first()
    if released.owner_id == current_user.id:
        released.owner_id = None
        db.session.commit()
        if released.nickname == '':
            flash(f'{released.name.title()} released successfully!', 'success')

        else:
            flash(f'{released.nickname} released successfully!', 'success')

    else:
        flash(f'Oops! Looks like you are not the owner of this Pokémon, so you are not permitted to release this one.', 'danger')
        return redirect(url_for('dex.collection'))

    return redirect(url_for('dex.available'))

@bp.route('/rename', methods=['POST'])
@login_required
def rename():
    id = request.form['renameID']
    renamed = Pokemon.query.filter_by(id=id).first()
    old_nick = renamed.nickname
    new_nick = request.form['newNick']

    if renamed.owner_id == current_user.id:
        renamed.nickname = new_nick
        db.session.commit()
        if old_nick == '':
            flash(f'{renamed.name.title()} was renamed successfully to {renamed.nickname}!', 'success')
        else:
            flash(f'{old_nick} was renamed successfully to {renamed.nickname}!', 'success')
    else:
        flash(f'Oops! Looks like you are not the owner of this Pokémon, so you are not permitted to rename this one.', 'danger')
        return redirect(url_for('dex.collection'))

    return redirect(url_for('dex.collection'))

@bp.route('/redescribe', methods=['POST'])
@login_required
def redesc():
    id = request.form['redescID']
    redesced = Pokemon.query.filter_by(id=id).first()
    new_desc = request.form['newDesc']

    if redesced.owner_id == current_user.id:
        redesced.description = new_desc
        db.session.commit()
        if redesced.nickname == '':
            flash(f'{redesced.name.title()} has a new description!', 'success')

        else:
            flash(f'{redesced.nickname} has a new description!', 'success')
            
    else:
        flash(f'Oops! Looks like you are not the owner of this Pokémon, so you are not permitted to give this one a new description.', 'danger')
        return redirect(url_for('dex.collection'))

    return redirect(url_for('dex.collection'))