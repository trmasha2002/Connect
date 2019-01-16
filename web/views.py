from web.forms import *
from web.models import *
from flask import render_template, redirect, make_response, request, session
from werkzeug.utils import secure_filename
from os import urandom
from base64 import b64encode
from web import app
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("main.html")


@app.route("/register", methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.user_name.data, form.password.data,
                                    form.link_for_connect.data, form.specialization.data, form.description.data, form.image.data)
        id = user.save()
        session['login'] = form.user_name.data
        session['is_auth'] = True
        session['id'] = id
        return redirect('/')
    return render_template("register.html", form=form)

@app.route("/add_idea", methods=['GET', 'POST'])
def add_idea():
    form = AddIdeaForm()
    if form.validate_on_submit():
        idea = Idea(form.name.data, form.small_description.data, form.description.data, form.image.data)
        id = idea.save()
        return redirect('/')
    return render_template("add_idea.html", form=form)

def g