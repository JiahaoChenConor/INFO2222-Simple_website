"""
    This file will handle our typical Bottle bottle.requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
"""

import bottle
import model
from verification import validate_picture
from io import BytesIO
import base64

app = application = bottle.Bottle()
cookie_secret = '1B32E674-443E-4602-89EA-643ACF6FD637'

# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@app.route('/img/<picture:path>')
def serve_pictures(picture):
    """
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the bottle.requested picture

        Returns a static file object containing the bottle.requested picture
    """
    return bottle.static_file(picture, root='static/img/')


# -----------------------------------------------------------------------------

# Allow CSS
@app.route('/css/<css:path>')
def serve_css(css):
    """
        serve_css

        Serves css from static/css/

        :: css :: A path to the bottle.requested css

        Returns a static file object containing the bottle.requested css
    """
    return bottle.static_file(css, root='static/css/')


# -----------------------------------------------------------------------------

# Allow javascript
@app.route('/js/<js:path>')
def serve_js(js):
    """
        serve_js

        Serves js from static/js/

        :: js :: A path to the bottle.requested javascript

        Returns a static file object containing the bottle.requested javascript
    """
    return bottle.static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------
@app.get('/knowledge')
def get_knowledge():
    return model.header(bottle.request, model.knowledge)


# Redirect to login
@app.get('/')
@app.get('/home')
def get_index():
    """
        get_index

        Serves the index page
    """
    return model.header(bottle.request, model.index)


# -----------------------------------------------------------------------------

# Display the login page
@app.get('/login')
def get_login_controller():
    """
        get_login

        Serves the login page
    """
    data = set_verification(bottle.response)
    return model.login_form(data)


# -----------------------------------------------------------------------------

# Attempt the login
@app.post('/login')
def post_login():
    """
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    """

    # Handle the form processing
    username = bottle.request.forms.get('username')
    if len(username) > 255:
        return model.header(bottle.request, model.custom_error, 'Username too long! ', '/login')
    password = bottle.request.forms.get('password')
    verification = bottle.request.forms.get('verification')
    true_verification = bottle.request.get_cookie('verification', secret=cookie_secret)
    if verification != true_verification:
        return model.header(bottle.request, model.custom_error, 'Wrong Verification! ', '/login')
    result = model.login_check(username, password)
    if result is not None:
        bottle.response.set_cookie("login", result[1], secret=cookie_secret)
        return model.header(bottle.request, model.custom_error,
                            'This username-password combination is valid, welcome! ', '/')
    else:
        return model.header(bottle.request, model.custom_error,
                            'This username-password combination is invalid, try again! ',
                            '/login')


# -----------------------------------------------------------------------------

# Display the register page
@app.get('/register')
def get_register_controller():
    """
        get_login

        Serves the login page
    """
    data = set_verification(bottle.response)
    return model.register_form(data)


# -----------------------------------------------------------------------------

# Attempt the register
@app.post('/register')
def post_login():
    # Handle the form processing
    username = bottle.request.forms.get('username')
    if len(username) > 255:
        return model.header(bottle.request, model.custom_error, 'Username too long! ', '/login')
    password = bottle.request.forms.get('password')
    password_confirmation = bottle.request.forms.get('password-confirmation')
    verification = bottle.request.forms.get('verification')
    true_verification = bottle.request.get_cookie('verification', secret=cookie_secret)
    if verification != true_verification:
        return model.header(bottle.request, model.custom_error, 'Wrong Verification! ', '/register')
    return model.register(username, password, password_confirmation)


# -----------------------------------------------------------------------------

@app.get('/about')
def get_about():
    """
        get_about

        Serves the about page
    """
    return model.header(bottle.request, model.about)


# -----------------------------------------------------------------------------

# Help with debugging
@app.post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@app.error(404)
def error(error):
    return model.handle_errors(error)


# -----------------------------------------------------------------------------

@app.get('/forum')
def forum_page():
    thread_id = bottle.request.query.thread_id
    data = set_verification(bottle.response)
    return model.header(bottle.request, model.forum_thread, thread_id, data)


@app.post('/forum')
def form_reply():
    verification = bottle.request.forms.get('verification')
    true_verification = bottle.request.get_cookie('verification', secret=cookie_secret)
    if verification != true_verification:
        return model.header(bottle.request, model.custom_error, 'Wrong Verification! ', '/forumtopic')
    cookie = bottle.request.get_cookie("login", secret=cookie_secret)
    user_id = model.verify_cookie(cookie)
    if user_id is None:
        return model.header(bottle.request, model.custom_error, 'You cannot reply if not logged in!', '/login')
    user_id = user_id[0]
    thread_id = bottle.request.query.thread_id
    comment = bottle.request.forms.get("comment")
    result = model.reply(thread_id, user_id, comment)
    if result:
        return model.header(bottle.request, model.custom_error, 'Reply successful!', '/forumtopic')
    else:
        return model.header(bottle.request, model.custom_error, 'Reply failed!', '/forumtopic')


# -----------------------------------------------------------------------------

@app.get('/forumtopic')
def forum_topic_page():
    topic_id = bottle.request.query.topic_id
    return model.header(bottle.request, model.forum_topic, bottle.request, topic_id)


# admin function delete post
@app.post('/forumtopic')
def delete_forum():
    is_admin = model.is_admin(bottle.request)
    if is_admin:
        thread_id = bottle.request.forms.get('thread_id')
        res = model.delete_post_by_id(thread_id)
        if res:
            return model.header(bottle.request, model.custom_error, 'Restoration/Deletion successful', '/forumtopic')
        else:
            return model.header(bottle.request, model.custom_error, 'Restoration/Deletion failed', '/forumtopic')
    return model.header(bottle.request, model.custom_error, 'Restoration/Deletion failed', '/forumtopic')


# -----------------------------------------------------------------------------

@app.get('/allusers')
def all_users_page():
    return model.header(bottle.request, model.all_users, bottle.request)


# admin function mute user
@app.post('/allusers')
def mute_user():
    is_admin = model.is_admin(bottle.request)
    if is_admin:
        user_id = bottle.request.forms.get('user_id')
        res = model.mute_user(user_id)
        if res:
            return model.header(bottle.request, model.custom_error, 'Mute/unmute successful', '/allusers')
        else:
            return model.header(bottle.request, model.custom_error, 'Mute/unmute failed', '/allusers')
    return model.header(bottle.request, model.custom_error, 'Mute/unmute failed', '/allusers')


# -----------------------------------------------------------------------------


@app.get('/post')
def post_page():
    data = set_verification(bottle.response)
    return model.header(bottle.request, model.post_get, data)


@app.post('/post')
def post_request():
    verification = bottle.request.forms.get('verification')
    true_verification = bottle.request.get_cookie('verification', secret=cookie_secret)
    if verification != true_verification:
        return model.header(bottle.request, model.custom_error, 'Wrong Verification! ', '/post')
    cookie = bottle.request.get_cookie("login", secret=cookie_secret)
    result = model.verify_cookie(cookie)
    if result is None:
        return model.header(bottle.request, model.custom_error, 'You cannot post if not logged in!', '/login')
    user_id = result[0]
    muted = result[4]
    if muted == 1:
        return model.header(bottle.request, model.custom_error, "You're Muted", '/post')
    thread_id = bottle.request.forms.get('thread_id')
    subject = bottle.request.forms.get('subject')
    if len(subject) > 255:
        return model.header(bottle.request, model.custom_error, "Subject too long", '/post')
    content = bottle.request.forms.get('content')
    result = model.post_post(user_id, thread_id, subject, content)
    if result:
        return model.header(bottle.request, model.custom_error, 'Post successful', '/forumtopic')
    else:
        return model.header(bottle.request, model.custom_error, 'Post failed', '/post')


def set_verification(response):
    img, code = validate_picture()
    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    data = str(base64.b64encode(buf_str))[1:].strip("'")
    response.set_cookie("verification", code, secret=cookie_secret)
    return data
