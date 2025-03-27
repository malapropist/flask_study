from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_blanked = db.Column(db.String(500))
    ref = db.Column(JSON)
    word_blank_positions = db.Column(JSON)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    score = db.Column(db.Integer)
    notes = db.relationship('Note')
    
