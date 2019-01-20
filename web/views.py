from web.models import *
from web import ma
from web import db
from web.models.user import UserSchema, User
from web.models.idea import IdeaSchema, Idea
from  web.models.session import SessionSchema, Session
from flask import render_template, redirect, make_response, request, session, jsonify
from werkzeug.utils import secure_filename
from os import urandom
from web import ma
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import datetime

now = datetime.datetime.now()
from base64 import b64encode
from web import app
auth = HTTPBasicAuth()
@app.route("/ideas", methods=['POST'])
def add_idea():
    name = request.json['name']
    small_description = request.json['small_description']
    description = request.json['description']
    image = request.json['image']

    idea = Idea(name, small_description, description, image)
    #idea.author_id = session['id']
    #idea.like()
    #print(session['id'])
    db.session.add(idea)
    db.session.commit()
    idea_schema = IdeaSchema()

    return idea_schema.jsonify(idea)
    #if form.validate_on_submit():
    #    idea = Idea(form.name.data, form.small_description.data, form.description.data, form.image.data)
    #    id = idea.save()
    #    return redirect('/')
    #return render_template("add_idea.html", form=form)

@app.route('/ideas/<int:idea_id>', methods=['GET'])
def get_by_id_idea(idea_id):
    idea_schema = IdeaSchema()
    idea = Idea.get_by_id(idea_id)
    return idea_schema.jsonify(idea)

@app.route('/my_ideas', methods=['GET'])
def get_my_ideas():
    ideas = db.session.query(Idea).filter(Idea.author_id == session['id']).all()
    ideas_schema = IdeaSchema(many=True)
    result = ideas_schema.dump(ideas)
    return jsonify(result.data)

@app.route('/favorites', methods=['GET'])
def get_favorites():
    ideas = db.session.query(Idea).filter(Idea.favorite == True).all()
    ideas_schema = IdeaSchema(many=True)
    result = ideas_schema.dump(ideas)
    return jsonify(result.data)

@app.route('/favorides<int:idea_id>', methods=['GET'])
def get_favorite_by_idea(idea_id):
    idea = get_by_id_idea(idea_id)

@app.route('/my_ideas/<int:idea_id>', methods=['GET'])
def get_my_idea_id(idea_id):
    idea = Idea.get_by_id(idea_id)
    idea_schema = IdeaSchema()
    result = idea_schema.dump(idea)
    return jsonify(result.data)

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


@app.route('/ideas', methods=['GET'])
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.get_all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)
    return jsonify(result.data)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(user_id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)

@app.route('/users', methods=['POST'])
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
    login = request.json.get('login')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.user_name == login).one()
    if (password == user.password):
        now = datetime.datetime.now()
        session = Session(user.id, user.token, str(now))
        session.save()
    session_shecma = SessionSchema()
    return session_shecma.jsonify(session)
    return jsonify({'status:':"OK"})
@app.route('/sessions', methods=['GET', 'POST'])
def get_sessions():
    sessions = Session.get_all()
    sessions_schema = SessionSchema(many=True)
    result = sessions_schema.dump(sessions)
    return jsonify(result.data)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_schema = UserSchema()
    user = User.get_by_id(user_id)
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

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_schema = UserSchema()
    user = User.get_by_id(user_id)
    user.delete()
    user_schema = UserSchema()
    return user_schema.jsonify(user)
