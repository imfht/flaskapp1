from flask import render_template
from flask_login import login_required
from server.blueprints import home


@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@home.route('/<path:path>', methods=['GET'])
def any_root_path(path):  # pylint: disable=unused-argument
    return render_template('index.html')


# hack for js routes
# todo: understand why any_root_path is not working correctly
@home.route('/login', methods=['GET'])
def login():
    return render_template('index.html')


@home.route('/register', methods=['GET'])
def register():
    return render_template('index.html')


@home.route('/feed', methods=['GET'])
def feed():
    return render_template('index.html')


@home.route('/profile', methods=['GET'])
def profile():
    return render_template('index.html')


@home.route('/twitter_callback', methods=['GET'])
@login_required
def twitter_callback():
    return render_template('index.html')


@home.route('/mastodon_auth_complete', methods=['GET'])
@login_required
def mastodon_auth_complete():
    return render_template('index.html')


@home.route('/privacy', methods=['GET'])
def privacy():
    return render_template('index.html')


@home.route('/about', methods=['GET'])
def about():
    return render_template('index.html')


@home.route('/forgot_password', methods=['GET'])
def forgot_password():
    return render_template('index.html')


@home.route('/reset_password?token=<token>', methods=['GET'])
def reset_password(token):  # pylint: disable=unused-argument
    return render_template('index.html')


@home.route('/fresh', methods=['GET'])
def stale_feed():
    return render_template('index.html')
