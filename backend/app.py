import configparser
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)

config = configparser.ConfigParser()
config.read('config.ini')

if not app.debug:
    config.read('config.production.ini')

app.config['SECRET_KEY'] = config['flask']['secret_key']

from mongoengine import connect
connect(**config['mongo'])

from handlers import errors
from handlers import post_handler
from handlers import user_handler

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
