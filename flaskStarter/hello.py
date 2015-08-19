__author__ = 'v-juponc'

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User : %s' % username

@app.route('/hello/<name>')
def hello(name=None):
	# This needs to be looked into as it dosen't make sense that this renders.
	# I'm likely not following the correct process and will have to check on it.
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run()
