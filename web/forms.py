from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
import re

class RegisterForm(FlaskForm):
    email = StringField(label="Email:", validators=[DataRequired(message='Это обязательное поле. name')])
    user_name = StringField(label="Имя пользователя:", validators=[DataRequired(message='Это обязательное поле. name')])
    password = StringField(label="Пароль:", validators=[DataRequired(message='Это обязательное поле. name')])
    link_for_connect = StringField(label="Ссылка для связи:", validators=[DataRequired(message='Это обязательное поле. name')])
    specialization = StringField(label="Специализация:", validators=[DataRequired(message='Это обязательное поле. name')])
    description =  StringField(label="Описание:", validators=[DataRequired(message='Это обязательное поле. name')])
    image = StringField(label="Картинка:", validators=[DataRequired(message='Это обязательное поле. name')])


class AddIdeaForm(FlaskForm):
    name = StringField(label="Название", validators=[DataRequired(message='Это обязательное поле. name')])
    small_description = StringField(label="Краткое описание", validators=[DataRequired(message='Это обязательное поле. name')])
    description = StringField(label="Описание:", validators=[DataRequired(message='Это обязательное поле. name')])
    image = StringField(label="Картинка", validators=[DataRequired(message='Это обязательное поле. name')])
