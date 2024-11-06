#!/usr/bin/python3
"""This script defines the endpoints for the RESTful api User service"""

from flask import Blueprint, jsonify, request, abort
from .models import User, users
import requests

user_bp = Blueprint('users', __name__)

# Helper function 1 to find user
def find_user(user_id):
    return next((user for user in users if user.id == user_id), None)

# Helper function 2 to validate user
def validate_user_data(data):
    if not data:
        abort(400, description="Request data is missing.")
    if 'username' not in data or not isinstance(data['username'], str) or not data['username'].strip():
        abort(400, description="Username is required and must be a non-empty string.")
    if 'email' not in data or not isinstance(data['email'], str) or not data['email'].strip():
        abort(400, description="Email is required and must be a non-empty string.")

# GET /users: Retrieve all users.
@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.__dict__ for user in users]), 200

# POST /users: Create a new user.
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    validate_user_data(data)

    user_id = len(users) + 1
    user = User(id=user_id, username=data['username'], email=data['email'])
    users.append(user)
    return jsonify(user.__dict__), 201

# Endpoint to fetch tasks for a user from the first service

@user_bp.route('/users/<int:id>/tasks', methods=['GET'])
def get_user_tasks(id):
    user = find_user(id)
    if user is None:
        abort(404, description="User not found")
    try:
        response = requests.get('http://127.0.0.1:5000/tasks')
        tasks = response.json()
    except requests.RequestException as e:
        return jsonify({"Error": "Couldn't connect to Tasks service"}), 503
    return jsonify(tasks), 200