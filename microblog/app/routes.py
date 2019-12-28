from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requisitado para o usuário {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)
