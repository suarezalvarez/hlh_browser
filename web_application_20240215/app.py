from flask import Flask, render_template, url_for, redirect
from model import db
import pymysql

# from uniprot_api import get_unipro_info_tuple
# from flask_bcrypt import bcrypt
# from flask_login import login_user, login_required, LoginManager, current_user

# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.exceptions import NotFound



def create_app():
    # Create a Flask app
    app = Flask(__name__)

    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/hlh'

    # Configure the SQLAlchemy instance with the Flask app
    db.init_app(app)

    return app