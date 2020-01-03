from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField('Diga algo', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Gravar')
