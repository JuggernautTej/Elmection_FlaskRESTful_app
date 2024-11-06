#!/usr/bin/python3
"""This script defines the endpoints for the RESTful api"""

from flask import Blueprint, jsonify, request, abort
from .models import Task, tasks

task_bp = Blueprint('tasks', __name__)

# Helper function 1
def find_task(task_id):
    return next((task for task in tasks if task.id == task_id), None)

# Helper function 2
def validate_task_data(data, is_update=False):
    if not data:
        abort(400, description="Request data is missing")
    if not is_update:
        if 'title' not in data or not isinstance(data['title'], str) or not data['title'].strip():
            abort(400, description="Title is required and must be a non-empty string")
        if 'description' not in data or not isinstance(data['description'],str):
            abort(400, description="Description is required and must be a string")
        if 'title' in data and (not isinstance(data['title'], str) or not data['title'].strip()):
            abort(400, description="Title must be a non-empty string.")
        if 'description' in data and not isinstance(data['description'], str):
            abort(400, description="Description must be a string.")
        if 'completed' in data and not isinstance(data['completed'], bool):
            abort(400, description="Completed must be a boolean.")    

# GET /tasks: Retrieve all tasks.
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.__dict__ for task in tasks]), 200

# GET /tasks/<id>: Retrieve a specific task by ID.
@task_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = find_task(id)
    if task is None:
        abort(404, description="Task not found.")
    return jsonify(task.__dict__), 200

# POST /tasks: Create a new task.
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    validate_task_data(data)

    task_id = len(tasks) + 1
    task = Task(id=task_id, title=data['title'], description=data['description'])
    tasks.append(task)
    return jsonify(task.__dict__), 201

# PATCH /tasks/<id>: Update a specific task.
@task_bp.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    task = find_task(id)
    if task is None:
        abort(404, description="Task not found.")
    data = request.get_json()
    validate_task_data(data, is_update=True)
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    return jsonify(task.__dict__), 200
