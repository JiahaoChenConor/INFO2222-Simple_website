# -*- coding: utf-8 -*
"""
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
"""
import view
import sql
import random
import markdown
import html
from hashlib import sha256

# Initialise our views, all arguments are defaults for the template
page_view = view.View()


# def knowledge():
#     return template("templates/knowledge.html")

def knowledge(header="header", username=None):
    """
        about
        Returns the view for the about page
    """
    return page_view("knowledge", header=header, username=username)

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------

def index(header="header", username=None):
    """
        index
        Returns the view for the index
    """
    return page_view("index", header=header, username=username)


# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------

def login_form(data):
    """
        login_form
        Returns the view for the login_form
    """
    return page_view("login", verification=data)


# -----------------------------------------------------------------------------
# Register
# -----------------------------------------------------------------------------

def register_form(data):
    """
        login_form
        Returns the view for the login_form
    """
    return page_view("register", verification=data)


# -----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    """
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns Cookie or None
    """
    sql_db = sql.SQLDatabase()
    password = sha256(password.encode()).hexdigest()
    res = sql_db.check_credentials(username, password)
    sql_db.close()
    return res


def valid(name, header="header", username=None):
    return page_view("valid", name=name, header=header, username=username)


def invalid():
    page_view("invalid", reason="Wrong Credentials")


# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------

def about(header="header", username=None):
    """
        about
        Returns the view for the about page
    """
    return page_view("about", garble=about_garble(), header=header, username=username)


# Returns a random string each time
def about_garble():
    """
        about_garble
        Returns one of several strings for the about page
    """
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
              "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
              "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
              "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
              "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
              "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


# -----------------------------------------------------------------------------
# Debug
# -----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


# -----------------------------------------------------------------------------
# 404
# Custom 404 error page
# -----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = html.escape(error.body)
    return page_view("error", error_type=error_type, error_msg=error_msg)


def custom_error(msg, link, header='header', username=None):
    return page_view("custom_error", msg=msg, link=link, header=header, username=username)


def verify_cookie(cookie):
    sql_db = sql.SQLDatabase()
    res = sql_db.cookie(cookie)
    sql_db.close()
    return res


def register(username, password, confirm_password):
    if password != confirm_password:
        return page_view("custom_error", msg="Registration failed, password not match! ", link='/register')
    sql_db = sql.SQLDatabase()
    password = sha256(password.encode()).hexdigest()
    result = sql_db.add_user(html.escape(username), password)
    sql_db.close()
    if result == "Done":
        return page_view("custom_error", msg="Registration complete, please login using your credentials",
                         link='/login')
    elif result == "Username already exists":
        return page_view("custom_error", msg="Registration failed, duplicated username", link='/register')
    else:
        return page_view("custom_error", msg="Registration failed, site error! ", link='/register')


# -----------------------------------------------------------------------------
# Forum Page
# -----------------------------------------------------------------------------

def forum_topic(request, topic_id=0, header='header', username=None):
    sql_db = sql.SQLDatabase()
    result = sql_db.query_post_by_id()
    sql_db.close()
    if len(result) == 0:
        return page_view("custom_error", msg='Empty topic', link='/', header=header, username=username)
    subject = result[0][0]
    admin = is_admin(request)
    topic_string = """
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 5px;
    text-align: left;    
    }
    </style>
    
    <div>
    <table class="table table-bordered table-dark">
    <thead class="thead-dark">
        <tr>
        <th scope="col">Subject</th>
        <th scope="col">Created at</th>
    """
    if admin:
        topic_string += "<th scope='col'>Delete Post</th>"
    topic_string += """
    </tr>
    </thead> 
    <tbody>"""
    n = 0
    for column in result:
        n += 1

        if admin:
            removed = ""
            button = "Remove"
            if column[3] == 1:
                removed = "[REMOVED]"
                button = "Restore"
            column_string = """
            <tr>
            <td><a href=/forum?thread_id={site}>{removed}{subject}</td>
            <td>{created_at}</td>
            <td>            
            <form action="" method="post">
            <input type="hidden" name="thread_id" value="{site}" />
            <input type="submit" value="{button}" id="delete_post">
            </form></td>
            </tr>
            """.format(removed=removed, site=column[0], subject=column[1], created_at=column[2], button=button)
        else:
            if column[3] == 1:
                continue
            column_string = """
            <tr>
            <td><a href=/forum?thread_id={site}>{subject}</td>
            <td>{created_at}</td>
            </tr>
            """.format(site=column[0], subject=column[1], created_at=column[2])
        topic_string += column_string

    topic_string += """
    </tbody>
    </table>
    </div>
    """

    topic_string += """
    <form action="/forum?topic_id={}" method="post">
    </form>
    """.format(topic_id)

    return page_view("forum_topic", subject=subject, body=topic_string, header=header, username=username)


def forum_thread(thread_id, data, header='header', username=None):
    sql_db = sql.SQLDatabase()
    result = sql_db.query_post_by_thread(thread_id)
    sql_db.close()
    if result[0][5] == 1:
        return page_view("custom_error", msg="Post removed. ", link="/forumtopic", header=header, username=username)
    subject = result[0][0]
    body = ""

    """
    <div class="card">
  <div class="card-header">
    Quote
  </div>
  <div class="card-body">
    <blockquote class="blockquote mb-0">
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
      <footer class="blockquote-footer">Someone famous in <cite title="Source Title">Source Title</cite></footer>
    </blockquote>
  </div>
</div>
    """
    for column in result:
        body += '<div class="card"><div class="card-header"><p>User {} Posted At: {}</p></div>\r\n'.format(column[4],
                                                                                                           column[2])
        body += '<div class="card-body">'
        body += markdown.markdown(column[1], extensions=['fenced_code'])
        body += '</div>\r\n</div>'
    body += """
    <form action="/forum?thread_id={}" method="post">
    <label for="comment">Post Your Comment:</label><br><br>
    <input type="text" name="comment" id="comment" style="width:90%;padding:5;height:50px;"><br><br>
    <img src="data:;base64,{}"><br><br>
    <input name="verification" type="text" placeholder="Verification" autocomplete="off"><br><br>
    <input type="submit" value="Submit" id="post">
    </form>
    """.format(thread_id, data)
    return page_view("forum", subject=subject, body=body, header=header, username=username)


# header
def header(request, func, *args):
    cookie = request.get_cookie("login", secret="1B32E674-443E-4602-89EA-643ACF6FD637")
    result = verify_cookie(cookie)
    if result is not None:
        return func(*args, header="header_logged_in", username=result[1])
    else:
        return func(*args)



# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------

def all_users(request, header='header', username=None):
    sql_db = sql.SQLDatabase()
    result = sql_db.query_all_users()
    sql_db.close()
    subject = result[0][0]
    admin = is_admin(request)
    if not admin:
        return page_view("users", subject=subject, body="<p>Hi, you're not an admin! </p>", header=header, username=username)
    body = """
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 5px;
    text-align: left;    
    }
    </style>
    
    <div>
    <table class="table table-bordered table-dark">
    <thead class="thead-dark">
        <tr>
        <th scope="col">Id</th>
        <th scope="col">Username</th>
        <th scope="col">Admin</th>
        <th scope="col">Muted</th>
        """
    if admin:
        body += """<th scope="col">Mute</th>"""
    body += """
    </tr>
    </thead> 
    <tbody>
    """

    for column in result:
        admin = "✅" if column[2] == 1 else "❎"
        muted = "✅" if column[3] == 1 else "❎"
        if admin:
            column_string = """
            <tr>
            <td>{id}</td>
            <td>{username}</td>
            <td>{admin}</td>
            <td>{muted}</td>
            <td>
            <form action="" method="post">
            <input type="hidden" name="user_id" value="{id}" />
            <input type="submit" value="Mute/Unmute" id="Mute/Unmute">
            </form></td>
            </tr>
            """.format(id=column[0], username=column[1], admin=admin, muted=muted)
            body += column_string
        else:
            column_string = """
            <tr>
            <td>{id}</td>
            <td>{username}</td>
            <td>{admin}</td>
            <td>{muted}</td>
            </tr>
            """.format(id=column[0], username=column[1], admin=admin, muted=muted)
            body += column_string

    body += """
    </tbody>
    </table>
    </div>
    """
    return page_view("users", subject=subject, body=body, header=header, username=username)


# -----------------------------------------------------------------------------
# Post
# -----------------------------------------------------------------------------

# admin-specific functions
def is_admin(request):
    cookie = request.get_cookie("login", secret="1B32E674-443E-4602-89EA-643ACF6FD637")
    result = verify_cookie(cookie)
    if result is not None and result[3] == 1:
        return True
    else:
        return False


def delete_post_by_id(thread_id):
    sql_db = sql.SQLDatabase()
    res = sql_db.delete_post_by_thread(thread_id)
    if res == "Database error":
        return False
    return True


def mute_user(user_id):
    sql_db = sql.SQLDatabase()
    res = sql_db.mute_user(user_id)
    if res == "Database error":
        return False
    return True


def post_get(data, header='header', username=None):
    return page_view("post", header=header, username=username, verification=data)


def post_post(user_id, thread_id, subject, content):
    sql_db = sql.SQLDatabase()
    result = sql_db.create_post(html.escape(subject), html.escape(content), thread_id, user_id)
    sql_db.close()
    return result


def reply(thread_id, user_id, content):
    sql_db = sql.SQLDatabase()
    result = sql_db.create_post("", html.escape(content), thread_id, user_id)
    sql_db.close()
    return result
