#!/usr/bin/python3
"""This script initializes the Flask application"""

from flask import Flask
from tasks.routes import task_bp

app = Flask(__name__)
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=True)