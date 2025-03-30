from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # ----- a route would create instances of forms and models and then render a template using those
    form = PostForm()
    if form.validate_on_submit():
        if current_user.get_username() in current_app.config['ADMIN_USERS']:
            post = Post(title=form.title.data, content=form.content.data, author=current_user, approved=1)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        if current_user.get_username() in current_app.config['ADMIN_USERS']:
            flash('Your post has been created!', 'success')
        else:
            flash('Your post is now being reviewed. It will appear on this page shortly', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.is_approved():
        # --- provide the variables into 'render_template()'
        #     which are needed in the context of the template
        return render_template('post.html', post=post)
    else:
        abort(404)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if current_user.get_username() not in current_app.config['ADMIN_USERS']:
            post.approved = 0
        db.session.commit()
        if current_user.get_username() in current_app.config['ADMIN_USERS']:
            flash('Your post has been updated!', 'success')
        else:
            flash('Your post is now being reviewed. It will appear on this page shortly', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # --- if updating post, need the title and content to be there
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


