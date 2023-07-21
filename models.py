# Connect to the SQLite database

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    signature = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    criminal_offence = db.Column(db.String(100), nullable=False)
   