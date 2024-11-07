#!/usr/bin/python3
"""This script initializes the Flask application"""

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from routes import task_bp
from bson.objectid import ObjectId

app = Flask(__name__)
app.register_blueprint(task_bp)

# MongoDB config
app.config["MONGO_URI"] = "mongodb://mongo:27017/tasks_db"
mongo = PyMongo(app)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = mongo.db.tasks.find()
    result = [{'_id': str(task['_id']), 'title': task['title'], 'description': task['description'], 'completed': task['completed']} for task in tasks]
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    if task:
        return jsonify({'_id': str(task['_id']), 'title': task['title'], 'description' : task['description'], 'completed': task['completed']})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<id>', methods=['PATCH'])
def update_task(id):
    data = request.json
    update_data = {k: v for k, v in data.items() if k in ['title', 'description', 'completed']}
    result = mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': update_data})
    if result.matched_count:
        return jsonify({'message': 'Task updated'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)