from mongoengine import Document, ListField, StringField
from passlib.hash import pbkdf2_sha256

def hash_password(password):
    # TODO real salt from config
    return pbkdf2_sha256.using(salt=b'super-secret').hash(password)

class User(Document):
    username = StringField(max_length=32, required=True)
    password = StringField(required=True)
