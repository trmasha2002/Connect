from itsdangerous import Serializer

from web import db, app
from web import ma
class Subscritions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    idea_id = db.Column(db.Integer(), db.ForeignKey("idea.id"))
    def __init__(self, user_id, idea_id):
        self.user_id = user_id
        self.idea_id = idea_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete()
        db.session.commit()

    @staticmethod
    def get_by_id(id_subscription):
        return db.session(Subscritions).filter(Subscritions.id == id_subscription).one()
    @staticmethod
    def get_all(self):
        return Subscritions.query.all()

class SubscriptionsSchema(ma.Schema):
     class Meta:
        fields = ('id', 'user_id', 'idea_id')