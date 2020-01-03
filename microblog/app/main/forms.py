from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from flask import request


class PostForm(FlaskForm):
    post = TextAreaField('Diga algo', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Gravar')


class SearchForm(FlaskForm):
    q = StringField('Buscar', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
