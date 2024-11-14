#!/usr/bin/python3
"""This script initializes the Flask application for the User resource service"""

from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from routes import user_bp
import requests

app = Flask(__name__)
#  app.register_blueprint(user_bp)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://mongo:27017/users_db"
mongo = PyMongo(app)

# Helper function to validate user
def validate_user_data(data):
    if not data:
        abort(400, description="Request data is missing.")
    if 'username' not in data or not isinstance(data['username'], str) or not data['username'].strip():
        abort(400, description="Username is required and must be a non-empty string.")
    if 'email' not in data or not isinstance(data['email'], str) or not data['email'].strip():
        abort(400, description="Email is required and must be a non-empty string.")

# Endpoint to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = [{'_id': str(user['_id']), 'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(result), 200

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    validate_user_data(data)

    user_id = mongo.db.users.insert_one({
        'username': data.get('username'),
        'email': data.get('email')
    }).inserted_id
    return jsonify({'_id': str(user_id)}), 201

# Endpoint to fetch tasks for a specific user
@app.route('/users/<id>/tasks', methods=['GET'])
def get_user_tasks(id):
    # This is a mock implementation;
    # mock_tasks = [
    #     {'task_id': 1, 'title': 'Task 1', 'description': 'First task', 'completed': False},
    #     {'task_id': 2, 'title': 'Task 2', 'description': 'Second task', 'completed': True}
    # ]
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if not user:
        abort(404, description="User not found")

    # communicate with the tasks service
    try:
        response = requests.get('http://tasks:5000/tasks')
        tasks = response.json()
    except requests.RequestException:
        return jsonify({"Error": "Couldn't connect to Tasks service"}), 503
    return jsonify({'user_id': id, 'tasks': tasks}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)