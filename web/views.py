import datetime

from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

from web import db
from web.models.dizlikes import Dizlikes, DizlikesSchema
from web.models.idea import IdeaSchema, Idea
from web.models.likes import Likes, LikesSchema
from  web.models.session import SessionSchema, Session
from web.models.subscriptions import Subscritions, SubscriptionsSchema
from web.models.user import UserSchema, User

now = datetime.datetime.now()
from web import app

auth = HTTPBasicAuth()
"""
def auth(token):
    return (len(db.session.query(Session).filter(Session.token == token).all()) > 0)
"""


@app.route("/ideas", methods=['POST'])
def add_idea():
    name = request.json['name']
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    small_description = request.json['small_description']
    description = request.json['description']
    image = request.json['image']
    idea = Idea(name, small_description, description, image)
    idea.author_id = user.id
    idea_schema = IdeaSchema()
    db.session.add(idea)
    db.session.commit()

    return idea_schema.jsonify(idea)


@app.route('/ideas', methods=['GET'])
def get_by_id_idea(idea_id):
    idea_schema = IdeaSchema()
    idea = Idea.get_by_id(idea_id)
    return idea_schema.jsonify(idea)


@app.route('/my_ideas', methods=['GET', 'POST'])
def get_my_ideas():
    token = request.headers['token']
    user = db.session.query(User).filter(User.token == token).one()
    ideas = db.session.query(Idea).filter(Idea.author_id == user.id).all()
    ideas_schema = IdeaSchema(many=True)
    result = ideas_schema.dump(ideas)
    return jsonify(result.data)


@app.route('/ideas/<int:idea_id>/make_favorite', methods=['POST'])
def make_favorite(idea_id):
    token = request.json['token']
    subscription_schema = SubscriptionsSchema()
    user = db.session.query(User).filter(User.token == token).one()
    print("Request user id is {} and idea id is {}".format(user.id, idea_id))
    idea = Idea.get_by_id(idea_id)
    if len(db.session.query(Subscritions).filter(Subscritions.user_id == user.id).filter(
                    Subscritions.idea_id == idea_id).all()) > 0:
        subscription = db.session.query(Subscritions).filter(Subscritions.user_id == user.id).filter(
            Subscritions.idea_id == idea_id).one()
        subscription.delete()
    else:
        subscription = Subscritions(user.id, idea_id)
        subscription.save()
    return subscription_schema.jsonify(subscription)


@app.route('/ideas/<int:idea_id>/favorites', methods=['GET', 'POST'])
def favorites(idea_id):
    users_schema = UserSchema(many=True)
    if len(db.session.query(Subscritions).filter(Subscritions.idea_id == idea_id).all()) > 0:
        subscriptions = db.session.query(Subscritions).filter(Subscritions.idea_id == idea_id).all()
        users = []
        for subscription in subscriptions:
            user = db.session.query(User).filter(User.id == subscription.user_id).one()
            users.append(user)
        result = users_schema.dump(users)
        print(result)
        return jsonify(result.data)
    else:
        return jsonify({[]})


@app.route('/favorite_ideas', methods=['GET', 'POST'])
def favorite_ideas():
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    if (len(db.session.query(Subscritions).filter(Subscritions.user_id == user.id).all()) > 0):
        subscriptions = db.session.query(Subscritions).filter(Subscritions.user_id == user.id).all()
        ideas = []
        for subscription in subscriptions:
            idea = db.session.query(Idea).filter(Idea.id == subscription.idea_id).one()
            ideas.append(idea)
        ideas_schema = IdeaSchema(many=True)
        result = ideas_schema.dump(ideas)
        return jsonify(result.data)


@app.route('/ideas/<int:idea_id>/like', methods=['GET', 'POST'])
def like(idea_id):
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    idea = Idea.get_by_id(idea_id)
    print(user.id, idea_id)
    if (len(db.session.query(Likes).filter(Likes.idea_id == idea_id).filter(Likes.user_id == user.id).all()) > 0):
        like = db.session.query(Likes).filter(Likes.idea_id == idea_id).filter(Likes.user_id == user.id).one()
        idea.likes -= 1
        idea.sum_diff -= 1
        like.delete()
    else:
        like = Likes(user.id, idea_id)
        idea.likes += 1
        idea.sum_diff += 1
        like.save()
    db.session.commit()
    like_schema = LikesSchema()
    return like_schema.jsonify(like)


@app.route('/ideas/<int:idea_id>/dizlike', methods=['GET', 'POST'])
def dizlike(idea_id):
    token = request.json['token']
    idea = Idea.get_by_id(idea_id)
    user = db.session.query(User).filter(User.token == token).one()
    if len(db.session.query(Dizlikes).filter(Dizlikes.idea_id == idea_id and Dizlikes.user_id == user.id).all()) > 0:
        dizlike = db.session.query(Dizlikes).filter(Dizlikes.idea_id == idea_id and Dizlikes.user_id == user.id).one()
        dizlike.delete()
        idea.sum_diff += 1
        idea.dizlikes -= 1
    else:
        dizlike = Dizlikes(user.id, idea_id)
        dizlike.save()
        idea.sum_diff -= 1
        idea.dizlikes += 1
    db.session.commit()
    dizlike_schema = DizlikesSchema()
    return dizlike_schema.jsonify(dizlike)


@app.route('/ideas/<int:idea_id>', methods=['PUT'])
def update_idea(idea_id):
    idea_schema = IdeaSchema()
    idea = Idea.get_by_id(idea_id)
    name = request.json['name']
    small_description = request.json['small_description']
    description = request.json['description']
    image = request.json['image']
    idea.name = name
    idea.small_description = small_description
    idea.description = description
    idea.image = image

    db.session.commit()

    return idea_schema.jsonify(idea)


@app.route('/ideas', methods=['POST'])
def get_ideas():
    ideas = Idea.get_all()
    ideas_schema = IdeaSchema(many=True)
    result = ideas_schema.dump(ideas)
    return jsonify(result.data)


@app.route('/ideas/<int:idea_id>', methods=['DELETE'])
def delete_by_id_idea(idea_id):
    idea = Idea.get_by_id(idea_id)
    idea.delete()
    idea_schema = IdeaSchema()
    return idea_schema.jsonify(idea)


@app.route('/users', methods=['POST'])
def get_users():
    users = User.get_all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)
    return jsonify(result.data)


@app.route('/profile', methods=['GET'])
def get_user():
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@app.route('/users', methods=['GET'])
def new_user():
    user_name = request.json.get('user_name')
    email = request.json.get('email')
    password = request.json.get('password')

    user = User(email, user_name, password)
    user.save()
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    session_shecma = SessionSchema()
    token = request.json.get('token')
    login = request.json.get('login')
    password = request.json.get('password')
    if (len(db.session.query(Session).filter(Session.token == token).all()) > 0):
        session = db.session.query(Session).filter(Session.token == token).one()
    else:
        user = db.session.query(User).filter(User.user_name == login).one()
        if (token == user.token or password == user.password):
            now = datetime.datetime.now()
            session = Session(user.id, user.token, str(now))
            session.save()
    return session_shecma.jsonify(session)


@app.route('/sessions', methods=['GET', 'POST'])
def get_sessions():
    sessions = Session.get_all()
    sessions_schema = SessionSchema(many=True)
    result = sessions_schema.dump(sessions)
    return jsonify(result.data)


@app.route('/users', methods=['PUT'])
def update_user():
    user_schema = UserSchema()
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    email = request.json['email']
    user_name = request.json['user_name']
    password = request.json['password']
    link_for_connect = request.json['link_for_connect']
    specialization = request.json['specialization']
    description = request.json['description']
    image = request.json['image']
    user.email = email
    user.user_name = user_name
    user.password = password
    user.link_for_connect = link_for_connect
    user.specialization = specialization
    user.description = description
    user.image = image
    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/users', methods=['DELETE'])
def delete_user():
    token = request.json['token']
    user = db.session.query(User).filter(User.token == token).one()
    user.delete()
    user_schema = UserSchema()
    return user_schema.jsonify(user)
