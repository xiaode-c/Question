from mongoengine import *
from datetime import datetime

connect("zhihudb")

class User(Document):
    name = StringField(max_length=80, required=True)
    email = StringField(required=True)
    created_time = DateTimeField(default=datetime.utcnow(), required=True)


class Question(Document):
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ReferenceField(User)
    tags = ListField(ReferenceField('Tag'))

class Answer(Document):
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(),required=True)
    author = ReferenceField(User)
    question = ReferenceField(Question)


class Comment(Document):
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ReferenceField(User)
    #answer = ReferenceField(Answer)
    #question = ReferenceField(Question)
    content_object = GenericReferenceField()

#class Category(Document):
#    name = StringField(max_length=100, required=True)
#    created_time = DateTimeField(default=datetime.utcnow(), required=True)
#    author = ReferenceFieldi

class Tag(Document):
    name = StringField(max_length=50, required=True)
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    edit_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ListField(ReferenceField(User))
    questions = ListField(ReferenceField(Question))
