from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.zhihudb

class User(object):

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.created_time = datetime.utcnow()

    def toBSON(self):
        doc = {"name":self.name,"email":self.email, "password":self.password, "created_time": self.created_time}
        return doc

class Question(object):

    def __init__(self, content, author_id, tags):
        self.md_content = content
        self.html_content = content
        self.created_time = datetime.utcnow()
        self.author_id = author_id
        self.tags = tags

    def toBSON(self):
        doc = {
            "md_content": self.md_content,
            "html_content": self.html_content,
            "created_time": self.created_time,
            "tags": self.tags,
            "author_id":self.author_id
        }

class Answer(object):

    def __init__(self, content, author_id, question_id):
        self.md_content = content
        self.html_content = content
        self.created_time = datetime.utcnow()
        self.author_id = author_id
        self.question_id = question_id

    def toBSON(self):
        doc = {
            "md_content": self.md_content,
            "html_content": self.html_content,
            "created_time": self.created_time,
            "author_id":self.author_id,
            "question_id":self.question_id
        }

class Comment(object):
    def __init__(self, content, author_id, answer_id=None, question_id=None, parent_id=None):
        self.md_content = content
        self.html_content = content
        self.created_time = datetime.utcnow()
        self.author_id = author_id
        self.parent_id = parent_id
        self.question_id = question_id
        self.anwser_id = answer_id

    def toBSON(self):
        if not self.parent_id:
            doc = {
                    "md_content": self.md_content,
                    "html_content": self.html_content,
                    "created_time": self.created_time,
                    "author_id": self.author_id,
                    "answer_id": self.question_id or self.anwser_id
                }
            return doc
        return {
                    "md_content": self.md_content,
                    "html_content": self.html_content,
                    "created_time": self.created_time,
                    "author_id": self.author_id,
                    "parent_id": self.parent_id,
                    "answer_id": self.question_id or self.anwser_id
                }

class Tag(object):

    def __init__(self, name, author, questions):
        self.name = name
        self.created_time = datetime.utcnow()
        self.edit_time = datetime.utcnow()
        self.author = author

    def toBSON(self):
        doc = {
            "name": self.name,
            "created_time": self.created_time,
            "edit_time": self.edit_time,
            "author":self.author
        }



