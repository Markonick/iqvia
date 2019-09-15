from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False, unique=False)
    last_name = db.Column(db.String(100), nullable=False, unique=False)
    emails = db.relationship('Email', backref='contacts', lazy=True, cascade='all')
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username=None, first_name=None, last_name=None, created=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.created = created


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)

    def __init__(self, address=None, ):
        self.address = address