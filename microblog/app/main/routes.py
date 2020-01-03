from datetime import datetime

from flask import (render_template, flash, redirect,
                   url_for, request, current_app)
from flask_login import current_user, login_required

from app import db
from app.main.forms import PostForm
from app.models import User, Post
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Sua postagem foi inserida!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Home',
                           form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Você não pode sequir a si mesmo!')
        return redirect(url_for('users.view', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Você está seguindo {}!'.format(username))
    return redirect(url_for('users.view', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Você não pode deixar de seguir a si mesmo!')
        return redirect(url_for('users.view', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Você deixou de seguir {}.'.format(username))
    return redirect(url_for('users.view', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
