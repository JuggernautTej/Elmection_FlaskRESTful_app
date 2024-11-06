#!/usr/bin/python3
"""This script defines the class to represent the User Resource structure"""

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

users = []