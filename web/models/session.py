from flask import jsonify

from web import db, app
from web import ma
from web.models import user
class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    login_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    token = db.Column(db.String())
    creation_date = db.Column(db.String())
    def __init__(self, login_id, token, creation_date):
        self.login_id = login_id
        self.token = token
        self.creation_date = creation_date

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_all():
        return Session.query.all()
    @staticmethod
    def get_by_id(self, id):
        return db.session.query(Session).filter(Session.id == id).one()

class SessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'login_id', 'token', 'creation_date')