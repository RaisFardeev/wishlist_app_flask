from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email, URL
from wishlist_app import bcrypt
from wishlist_app.models import User, Wish


class RegistrationForm(FlaskForm):
    name = StringField('Имя',
                       validators=[DataRequired(), Length(min=1, max=20)],
                       render_kw={"placeholder": "Введите имя"})
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=10, max=30)],
                        render_kw={"placeholder": "Введите email"})
    password1 = PasswordField('Пароль',
                              validators=[DataRequired(), Length(min=1, max=20)],
                              render_kw={"placeholder": "Введите пароль"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), Length(min=1, max=20)],
                              render_kw={"placeholder": "Введите пароль еще раз"})
    submit = SubmitField('Зарегестрироваться')

    def validate_email(self, *args):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors += 'Пользователь с таким адресом уже существует'

    def validate_password(self, *args):
        if self.password1.data != self.password2.data:
            self.password1.errors += 'Пароли не совпадают'


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=10, max=30)],
                        render_kw={"placeholder": "Введите email"})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=1, max=20)],
                             render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Log In')

    def validate_(self, *args):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors += 'что-то не так с адресом'
        if not bcrypt.check_password_hash(self.password.data, user.password):
            self.password.errors += 'что-то не так с паролем'


class WishCreateForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Введите название"})
    description = TextAreaField('Описание',
                                validators=[DataRequired(), Length(max=300)],
                                render_kw={"placeholder": "Введите описание"})
    price = IntegerField('Цена',
                         validators=[DataRequired(), NumberRange(min=0)],
                         render_kw={"placeholder": "Введите цену"})
    url = StringField('Url',
                        validators=[DataRequired(), URL(), Length(min=10, max=100)],
                        render_kw={"placeholder": "Введите URL"})
    submit = SubmitField('Создать')


class WishEditForm(FlaskForm):
    name = StringField('Название',
                       validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Введите название"})
    description = TextAreaField('Описание',
                                validators=[DataRequired(), Length(max=300)],
                                render_kw={"placeholder": "Введите описание"})
    price = IntegerField('Цена',
                         validators=[DataRequired(), NumberRange(min=0)],
                         render_kw={"placeholder": "Введите цену"})
    url = StringField('Url',
                        validators=[DataRequired(), URL(), Length(min=10, max=100)],
                        render_kw={"placeholder": "Введите URL"})
    submit = SubmitField('Изменить')
