from web import db
from web import ma
from web import app

class Dizlikes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    idea_id = db.Column(db.Integer(), db.ForeignKey("idea.id"))

    def __init__(self, user_id, idea_id):
        self.user_id = user_id
        self.idea_id = idea_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(like_id):
        return db.session.query(Dizlikes).filter(Dizlikes.id == like_id).one()


class DizlikesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'idea_id')

