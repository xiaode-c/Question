# coding:utf-8

from mongoengine import *
from datetime import datetime
from . import login_manager

connect("zhihudb")


class Pagination(object):

    def __init__(self, total, page, itemNum):
        self.page = page
        self.itemNum = itemNum
        self.total = total

    @property
    def has_prev(self):
        return self.page != 1

    @property
    def has_next(self):
        return self.page * self.itemNum < self.total.count()

    @property
    def items(self):
        return self.total.skip((self.page-1)*self.itemNum).limit(self.itemNum)

    @property
    def pages(self):
        total = self.total.count()
        return total / self.itemNum \
            if (total % self.itemNum == 0) \
            else total / self.itemNum + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages+1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and
                        num < self.page+right_current) or \
                    num > self.pages - right_edge:
                if last+1 != num:
                    yield None
                yield num
                last = num

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1


class PaginationMixin(object):

    @classmethod
    def pagination(cls, page, itemNum):
        total = cls.objects
        return Pagination(total, page, itemNum)


class User(Document):
    name = StringField(max_length=80, required=True)
    email = StringField(required=True)
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    password = StringField(max_length=80)

    @staticmethod
    def generate_fake(count=10):
        from random import seed
        from faker import Factory
        fake = Factory.create('zh_CN')
        seed()
        for i in range(count):
            user = User(name=fake.name(), email=fake.email(),
                        created_time=fake.date_time_this_year(before_now=True,
                                                              after_now=False))
            user.save()

    # 下面是Flask-Login需要的方法
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # User类中自动添加的id
    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name


class Question(Document, PaginationMixin):
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ReferenceField(User)
    tags = ListField(ReferenceField('Tag'))

    @staticmethod
    def generate_fake(count=50):
        from random import seed, randint
        from faker import Factory
        fake = Factory.create('zh_CN')
        seed()
        user_count = User.objects.count()
        tag_count = Tag.objects.count()
        for i in range(count):
            u = User.objects[randint(0, user_count-1)]
            t = Tag.objects[randint(0, tag_count-1)]
            quest = Question(content=fake.text(max_nb_chars=1000),
                             created_time=fake.date_time(),
                             author=u
                             )
            quest.tags = [t]
            quest.save()


class Answer(Document):
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ReferenceField(User)
    question = ReferenceField(Question)

    @staticmethod
    def generate_fake(count=50):
        from random import seed, randint
        from faker import Factory
        fake = Factory.create('zh_CN')
        seed()
        user_count = User.objects.count()
        question_count = Question.objects.count()
        for i in range(count):
            u = User.objects[randint(0, user_count-1)]
            q = Question.objects[randint(0, question_count-1)]
            a = Answer(content=fake.text(max_nb_chars=500),
                       created_time=fake.date_time_this_year(before_now=True,
                                                             after_now=False),
                       author=u,
                       question=q)
            a.save()


class Comment(Document):
    # parent_comment = ReferenceField(Comment)
    content = StringField()
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ReferenceField(User)
    answer = ReferenceField(Answer)
    question = ReferenceField(Question)
    content_object = GenericReferenceField()


# def render_tree(obj, tree):
#     for o in obj:
#         if o.parent_comment==None:
#             tree[obj] = None
#         else:
#             render_tree(o, tree)
#     return tree

# def comment_tree(question_or_answer):
#     tree = []
#     for obj in question_or_answer:
#         if obj.parent_comment = None:
#             tree[obj] = None
#         else:
#             tree[obj] = obj.parent_comment


# class Category(Document):
#    name = StringField(max_length=100, required=True)
#    created_time = DateTimeField(default=datetime.utcnow(), required=True)
#    author = ReferenceFieldi

class Tag(Document):
    name = StringField(max_length=50, required=True)
    created_time = DateTimeField(default=datetime.utcnow(), required=True)
    edit_time = DateTimeField(default=datetime.utcnow(), required=True)
    author = ListField(ReferenceField(User))
    questions = ListField(ReferenceField(Question))

    @staticmethod
    def generate_fake(count=50):
        from random import seed, randint
        from faker import Factory
        fake = Factory.create('zh_CN')
        seed()
        user_count = User.objects.count()
        for i in range(count):
            u = User.objects[randint(0, user_count-1)]
            tag = Tag(name=fake.word(),
                      created_time=fake.date_time_this_year(before_now=True,
                                                            after_now=False),
                      author=[u])
            tag.save()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()
