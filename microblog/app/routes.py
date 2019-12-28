from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Francisco'}
    posts = [
        {
            'author': {'username': 'João'},
            'body': 'Um lindo dia em São Paulo!'
        },
        {
            'author': {'username': 'Luiz'},
            'body': 'Vingador foi um ótimo filme!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
