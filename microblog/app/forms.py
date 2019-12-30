from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    about_me = TextAreaField('Sobre mim', validators=[Length(min=0, max=140)])
    submit = SubmitField('Gravar')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Por favor, use um nome diferente.')


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembre-me de mim')
    submit = SubmitField('Logar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirme a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Gravar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um nome diferente')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor use um e-mail diferente.')
