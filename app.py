from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ

# initialize app
app = Flask(__name__)

# set SQLALCHEMY_DATABASE_URI key
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///research_notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
# create db file
db = SQLAlchemy(app)

app.static_folder = 'static'

# create login manager
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def welcome():
    return render_template('welcome.html')



