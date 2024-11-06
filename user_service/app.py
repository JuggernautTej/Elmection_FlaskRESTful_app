#!/usr/bin/python3
"""This script initializes the Flask application for the User resource service"""

from flask import Flask
from routes import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://mongo:27017/users_db"
mongo = PyMongo(app)
if __name__ == '__main__':
    app.run(port=50001, debug=True)