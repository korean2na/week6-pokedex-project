from app import db
from datetime import datetime

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50), nullable=False)
    poke_num = db.Column(db.Integer, nullable=False)
    type1 = db.Column(db.String(50), nullable=False)
    type2 = db.Column(db.String(50))
    sprite = db.Column(db.String(1000), nullable=False)
    nickname = db.Column(db.String(50))
    description = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='pokemon')
