from flask import Blueprint

bp = Blueprint('dex', __name__, url_prefix='/dex')

from . import routes,models
