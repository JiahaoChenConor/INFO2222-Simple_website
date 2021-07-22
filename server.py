from bottle import route, run, static_file, template


@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('hello_template', name=name)


@route('/aboutus')
def aboutus():
    return static_file('aboutus', root='/')


if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True)
