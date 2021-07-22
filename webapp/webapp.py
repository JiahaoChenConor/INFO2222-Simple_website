from bottle import route, run, template, static_file, url, default_app, request, get, post
import bottle
import os
import sys

def calculate_something(input_data):
    return "the answer"

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
print(dir_path)

if(sys.platform == 'win32'):
    templates_dir = os.path.join(dir_path, 'views')
    if templates_dir not in bottle.TEMPLATE_PATH:
        bottle.TEMPLATE_PATH.insert(0, templates_dir)
    # the code above allows the same file layout to be used on the localhost and 
    # pythonanywhere site. In the app directory is wsgi.py and two directories
    # static and views.  Static has the css/js/images, views contains index.html
    # on pythonanywhere the bottle.TEMPLATE_PATH is set in the app_wsgi.py file
    # located at /var/www

@route('/')
def home():
    ''' A bit of documentation
    '''
    return template('index.html')

@route('/static/<filename:path>')
def send_static(filename):
    ''' This makes the extant template start working
       Woo-Hoo!
    '''
    return static_file(filename, root= dir_path + '/static/') 
    # the dir_path+'/'+ needed to be added to get this to serve static pages on PythonAnywhere
    # also I had to create a 'views' directory and put the index.html file into the views directory

@route('/hello')
def hello():
    ''' A bit of documentation
    '''
    return '<h1>Hello World!</h1>'

@route('/hello/', method='GET')
def hello():
    ''' A bit of documentation
    '''
    return '<h1>Hello World (two slash...) !</h1>'

@route('/location', method = 'POST')
def location():
    return calculate_something(input_data)

#
# the lines below recommended by PythonAnywhere forum for Bottle webapp
#

application = default_app()
if __name__ == '__main__':
    bottle.debug(True)                              # remove this for production
    bottle.run(host='0.0.0.0', port=8080)