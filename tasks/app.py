#!/usr/bin/python3
"""This script initializes the Flask application"""

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from tasks.routes import task_bp
from bson.objectid import ObjectId

app = Flask(__name__)
app.register_blueprint(task_bp)

# MongoDB config
app.config["MONGO_URI"] = "mongodb://mongo:27017/tasks_db"
mongo = PyMongo(app)

@app.route('/tasks', methods=['GET'])
def get_task(id):
    tasks = mongo.db.tasks.find()
    result = [{'_id': str(task['_id']), 'title': task['title'], 'description': task['description'], 'completed': task['completed']} for task in tasks]
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):

if __name__ == '__main__':
    app.run(debug=True)