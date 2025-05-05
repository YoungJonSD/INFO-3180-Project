from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    profiles = db.relationship('Profile', backref='user', lazy=True)
    favorited_by = db.relationship('Favourite', backref='favorited_user',lazy=True, foreign_keys='Favourite.fav_user_id_fk')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'photo': self.photo,
            'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    parish = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(80), nullable=False)
    fav_colour = db.Column(db.String(80), nullable=False)
    fav_school_sibject = db.Column(db.String(80), nullable=False)
    political = db.Column(db.Boolean, nullable=False)
    religious = db.Column(db.Boolean, nullable=False)
    family_oriented = db.Column(db.Boolean, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id_fk,
            'description': self.description,
            'parish': self.parish,
            'biography': self.biography,
            'sex': self.sex,
            'race': self.race,
            'birth_year': self.birth_year,
            'height': self.height,
            'fav_cuisine': self.fav_cuisine,
            'fav_colour': self.fav_colour,
            'fav_school_sibject': self.fav_school_sibject,
            'political': self.political,
            'religious': self.religious,
            'family_oriented': self.family_oriented,
        }

class Favourite(db.Model):
    __tablename__ = 'favourites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id_fk,
            'fav_user_id': self.fav_user_id_fk,
        }