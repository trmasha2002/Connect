from sqlalchemy import desc

from web import app
from web import db
from web import ma
from web.models.user import User
class Idea(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    small_description = db.Column(db.String())
    description = db.Column(db.String())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String())
    likes = db.Column(db.Integer())
    dizlikes = db.Column(db.Integer())
    sum_diff = db.Column(db.Integer())
    def __init__(self, name, small_description, description, image):
        self.name = name
        self.small_description = small_description
        self.description = description
        self.image = image
        self.likes = 0
        self.dizlikes = 0
        self.sum_diff = 0
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return db.session.query(Idea).filter(Idea.id == id).one()

    @staticmethod
    def update_by_id(id, key, value):
        db.session.query(Idea).filter(Idea.id == id).update({key:value},  synchronize_session='evaluate')

    @staticmethod
    def get_all():
        print(Idea.query.all())
        print(Idea.query.order_by(desc('sum_diff')))
        return Idea.query.order_by(desc('sum_diff'))
class IdeaSchema(ma.Schema):
    class Meta:
        fields = ('name', 'author_id', 'small_description', 'description', 'image', 'likes', 'dizlikes', 'id')
