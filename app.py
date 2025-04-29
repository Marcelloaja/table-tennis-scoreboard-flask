import os
import logging
from flask import Flask
from extensions import db

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///table_tennis.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Init database with app
db.init_app(app)

# Import routes to register all views
with app.app_context():
    from models import Player, Match
    db.create_all()

# Penting: import routes setelah inisialisasi app & db
from routes import *

if __name__ == '__main__':
    app.run(debug=True)