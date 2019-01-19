from web import db
from web import ma
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String())
    user_name = db.Column(db.String())
    password = db.Column(db.String())
    link_for_connect = db.Column(db.String())
    specialization = db.Column(db.String())
    description = db.Column(db.String())
    image = db.Column(db.String())

    def __init__(self, email, user_name, password, link_for_connect, specialization, description, image):
        self.email = email
        self.user_name = user_name
        self.password = password
        self.link_for_connect = link_for_connect
        self.specialization = specialization
        self.description = description
        self.image = image

    def save(self):
        db.session.add(self)
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'user_name', 'password', 'link_for_connect', 'specialization', 'description', 'image', 'id')

