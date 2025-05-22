# app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10))  # 'owner' or 'farmer'
    name = db.Column(db.String(100))
    village = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    # Relationship: One owner can have many harvesters
    harvesters = db.relationship('Harvester', backref='owner', lazy=True)

class Harvester(db.Model):
    __tablename__ = 'harvester'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(100))
    vehicle_number = db.Column(db.String(50))
    contact = db.Column(db.String(20))
