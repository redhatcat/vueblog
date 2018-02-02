from datetime import datetime
from mongoengine import (
    Document,
    DateTimeField,
    IntField,
    ListField,
    StringField,
    signals,
)
from models.util import mongo_to_dict

class Post(Document):
    title = StringField(max_length=120, required=True)
    slug = StringField(max_length=120, required=True, unique=True)
    body = StringField()
    author = StringField(max_length=120)
    tags = ListField(StringField(max_length=30))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    published_at = DateTimeField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

    def to_dict(self):
       return mongo_to_dict(self)

signals.pre_save.connect(Post.pre_save, sender=Post)
