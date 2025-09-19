import os
from flask import Flask, session
from main.api import api_bp

app = Flask(
    __name__,
    static_folder='static')

app.secret_key = os.environ.get('SECRET_KEY', 'SECRET_KEY')
app.register_blueprint(api_bp)

# setup configs
env = os.environ.get('FLASK_ENV', 'development')

app.config['ENV'] = env
app.config.from_pyfile(f'config/{env}.cfg')
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

print(f"Database URL being used: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
print(f"Redis URL being used: {app.config.get('REDIS_URL')}")
# CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf_protect = CSRFProtect(app)

# Database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECURITY_REGISTERABLE'] = True

from flask_sslify import SSLify
if os.environ.get('FLASK_ENV') != 'development':
    ssl = SSLify(app)
app.config['WTF_CSRF_ENABLED'] = False
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask_minify import Minify
minify = Minify(app=app, passive=True)

