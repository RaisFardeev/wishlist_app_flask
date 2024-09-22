import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from dotenv import load_dotenv


load_dotenv()
db_name = os.getenv("DB_NAME")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

basedir = os.path.abspath(os.path.dirname(__file__))
bcrypt = Bcrypt()
#
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '2e343t54ytgfe3r54oigth'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=3600*2)

db = SQLAlchemy(app)
Session(app)
from . import routes, models
with app.app_context():
    db.create_all()
print(db)