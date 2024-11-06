#!/usr/bin/python3
"""This script defines the class to represent the task resource"""

class Task:
    def __init__(self, id, title, description, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

tasks = []