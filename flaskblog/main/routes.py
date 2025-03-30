import os
from datetime import datetime

from flask import render_template, request, Blueprint, g, url_for, current_app, send_from_directory
from flask_babel import get_locale
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import SearchForm
from flaskblog.utils import create_sentiment_index_plot

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.before_app_request
def before_request():
    # if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
    g.search_form = SearchForm()
    g.locale = str(get_locale())


@main.route('/search')
def search():
    # if not g.search_form.validate():
    #     return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', posts=posts,
                           next_url=next_url, prev_url=prev_url)


@main.route("/about")
def about():
    return render_template("about.html", title='About')
