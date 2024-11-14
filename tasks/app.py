#!/usr/bin/python3
"""This script initializes the Flask application"""

from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
# from routes import task_bp
from bson.objectid import ObjectId

app = Flask(__name__)
# app.register_blueprint(task_bp)

# MongoDB config
app.config["MONGO_URI"] = "mongodb://mongo:27017/tasks_db"
mongo = PyMongo(app)

# Helper function to validate incoming data
def validate_task_data(data, is_update=False):
    if not data:
        abort(400, description="Request data is missing")
    if not is_update:
        if 'title' not in data or not isinstance(data['title'], str) or not data['title'].strip():
            abort(400, description="Title is required and must be a non-empty string")
        if 'description' not in data or not isinstance(data['description'],str):
            abort(400, description="Description is required and must be a string")
    if 'completed' in data and not isinstance(data['completed'], bool):
        abort(400, description="Completed must be a boolean.")   

# Endpoint to retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = mongo.db.tasks.find()
    result = [
        {'_id': str(task['_id']), 'title': task['title'], 'description': task['description'], 'completed': task['completed']} 
        for task in tasks]
    return jsonify(result), 200

# Endpoint to retrieve a specific task by ID
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    if task:
        return jsonify(
            {'_id': str(task['_id']), 'title': task['title'], 'description' : task['description'], 'completed': task['completed']}), 200
    return jsonify({'error': 'Task not found'}), 404

# Endpoint to create a new task.
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    validate_task_data(data)
    task = { 
        'title': data['title'],
        'description': data['description'],
        'completed': data.get('completed', False)}
    result = mongo.db.tasks.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return jsonify(task), 201

# Endpoint to update a specific task by ID
@app.route('/tasks/<id>', methods=['PATCH'])
def update_task(id):
    data = request.get_json
    validate_task_data(data, is_update=True)
    update_data = {k: v for k, v in data.items() if k in ['title', 'description', 'completed']}
    result = mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': update_data})
    if result.matched_count:
        return jsonify({'message': 'Task updated'}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)