#!/usr/bin/python3
"""This script defines the endpoints for the RESTful api"""

from flask import Blueprint, jsonify, request, abort
from .models import Task, tasks

task_bp = Blueprint('tasks', __name__)

def find_task(task_id):
    return next((task for task in tasks if task.id == task_id), None)

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
    if not data or 'title' not in data or 'description' not in data:
        abort(400, description="Title and description are required fields.")
    task_id = len(tasks) + 1
    task = Task(id=task_id, title=data['title'], description=data['description'])
    tasks.append(task)
    return jsonify(task.__dict__), 201

# PATCH /tasks/<id>: Update a specific task.
@task_bp.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    return