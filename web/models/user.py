from itsdangerous import Serializer

from web import db, app
from web import ma
from passlib.hash import pbkdf2_sha256
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String())
    user_name = db.Column(db.String())
    password = db.Column(db.String())
    link_for_connect = db.Column(db.String())
    specialization = db.Column(db.String())
    description = db.Column(db.String())
    image = db.Column(db.String())
    token = db.Column(db.String())
    def __init__(self, email, user_name, password):
        self.email = email
        self.user_name = user_name
        self.password = password
        self.token = pbkdf2_sha256.hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return db.session.query(User).filter(User.id == id).one()
    @staticmethod
    def update_by_id(id, key, value):
        return db.session.query(User).filter(User.id == id).update({key: value},synchronize_session='evaluate')
    @staticmethod
    def get_all():
        return User.query.all()

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'user_name', 'password', 'link_for_connect', 'specialization', 'description', 'image', 'id', 'token')

