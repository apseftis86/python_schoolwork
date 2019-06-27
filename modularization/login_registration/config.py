from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)