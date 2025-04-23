from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON, Enum
import enum

# Define possible roles
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="Untitled Verse")
    data = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_blanked = db.Column(db.String(500))
    ref = db.Column(JSON)
    word_blank_positions = db.Column(JSON)
    completions = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    score = db.Column(db.Integer)
    role = db.Column(Enum(UserRole), default=UserRole.USER)
    notes = db.relationship('Note')
    weekly_score = db.Column(db.Integer, default=0)
    
