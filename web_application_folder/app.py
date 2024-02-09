from flask import Flask, render_template, url_for, redirect
from config import config, PREFIX
from model import db, User, Userdata, Seqanalysis
from forms import SignUpForm, LoginForm, SearchForm
#from uniprot_api import get_unipro_info_tuple
from flask_bcrypt import bcrypt
from flask_login import login_user, login_required, LoginManager, current_user

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound