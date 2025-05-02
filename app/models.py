from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    photo = db.Column(db.String(256))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(256))
    parish = db.Column(db.String(64))
    biography = db.Column(db.String(512))
    sex = db.Column(db.String(10))
    race = db.Column(db.String(64))
    birth_year = db.Column(db.Integer)
    height = db.Column(db.Float)
    fav_cuisine = db.Column(db.String(64))
    fav_colour = db.Column(db.String(64))
    fav_school_sibject = db.Column(db.String(64))
    political = db.Column(db.Boolean)
    religious = db.Column(db.Boolean)
    family_oriented = db.Column(db.Boolean)

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
