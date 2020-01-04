from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.users import bp
from app.users.forms import EditProfileForm
from app.models import User, Post


@bp.route('/view/<username>')
@login_required
def view(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('users.view', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('users.view', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('users/view.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('As alterações foram gravadas com sucesso.')
        return redirect(url_for('users.edit'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('users/edit.html', title='Edit Profile',
                           form=form)


@bp.route('/view/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users/view_popup.html', user=user)
