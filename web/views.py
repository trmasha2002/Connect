from web.forms import *
from web.models import *
from web import ma
from web.models import UserSchema
from flask import render_template, redirect, make_response, request, session, jsonify
from werkzeug.utils import secure_filename
from os import urandom
from base64 import b64encode
from web import app
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("main.html")


#@app.route("/register", methods=['GET', 'POST'])
#def registration():
#    form = RegisterForm()
#    if form.validate_on_submit():
#        user = User(form.email.data, form.user_name.data, form.password.data,
#                                    form.link_for_connect.data, form.specialization.data, form.description.data, form.image.data)
#       id = user.save()
#        session['login'] = form.user_name.data
#        session['is_auth'] = True
#        session['id'] = id
#        return redirect('/')
#    return render_template("register.html", form=form)


@app.route("/users", methods=["POST"])
def add_user():
    user_name = request.json['user_name']
    email = request.json['email']
    password = request.json['password']
    link_for_connect = request.json['link_for_connect']
    specialization = request.json['specialization']
    description = request.json['description']
    image = request.json['image']
    user = User(email, user_name, password, link_for_connect, specialization, description, image)
    id = user.save()
    session['login'] = user_name
    session['is_auth'] = True
    session['id'] = id
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@app.route("/ideas", methods=['POST'])
def add_idea():
    name = request.json['name']
    small_description = request.json['small_description']
    description = request.json['description']
    image = request.json['image']

    idea = Idea(name, small_description, description, image)
    idea.author_id = session['id']
    print(session['id'])
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    print(users)
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)
    return jsonify(result.data)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_by_id_user(user_id):
    user = User.get_by_id(user_id)
    users_schema = UserSchema()
    result = users_schema.dump(user)
    return jsonify(result.data)
@app.route('/ideas/<int:idea_id>', methods=['DELETE'])

def delete_by_id_idea(idea_id):
    idea = Idea.get_by_id(idea_id)
    idea.delete()
    idea_schema = IdeaSchema()
    return idea_schema.jsonify(idea)