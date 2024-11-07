from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from configure.Config import Config

# Flask App Configuration
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db_pgl = SQLAlchemy(app)

from app.routes import application
