#!/usr/bin/python3
"""This script initializes the Flask application for the User resource service"""

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from routes import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://mongo:27017/users_db"
mongo = PyMongo(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = [{'_id': str(user['_id']), 'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(result)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = mongo.db.users.insert_one({
        'username': data.get('username'),
        'email': data.get('email')
    }).inserted_id
    return jsonify({'_id': str(user_id)}), 201

@app.route('/users/<id>/tasks', methods=['GET'])
def get_user_tasks(id):
    # This is a mock implementation;
    mock_tasks = [
        {'task_id': 1, 'title': 'Task 1', 'description': 'First task', 'completed': False},
        {'task_id': 2, 'title': 'Task 2', 'description': 'Second task', 'completed': True}
    ]
    return jsonify({'user_id': id, 'tasks': mock_tasks})

if __name__ == '__main__':
    app.run(port=50001, debug=True)