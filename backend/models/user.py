from mongoengine import Document, ListField, StringField
from passlib.hash import pbkdf2_sha256
from app import app

def hash_password(password):
    return pbkdf2_sha256.using(salt=bytes(app.config['SECRET_KEY'], 'utf-8')).hash(password)

class User(Document):
    username = StringField(max_length=32, required=True)
    password = StringField(required=True)
