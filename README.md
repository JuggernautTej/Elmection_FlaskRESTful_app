
----------

# Microservices Project: Task and User Management

This project consists of two Flask-based microservices:

1.  **Task Management Service**: Handles task creation, retrieval, and updates.
2.  **User Management Service**: Manages user creation and retrieval and provides mock task assignments.

These services are designed to demonstrate basic microservice architecture, RESTful API design, and inter-service communication.

## Table of Contents

-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Requirements](#requirements)
-   [Installation and Setup](#installation-and-setup)
-   [Running the Services](#running-the-services)
-   [Endpoints](#endpoints)
-   [Assumptions](#assumptions)
-   [Future Improvements](#future-improvements)

## Project Overview

This project uses two microservices that interact with each other to simulate user-task management. The **Task Management Service** allows users to create and manage tasks, while the **User Management Service** manages users and includes an endpoint that simulates tasks assigned to a user.

## Features

### Task Management Service

-   **Create, retrieve, and update tasks**
-   Each task includes:
    -   `id`: Unique identifier
    -   `title`: Task title
    -   `description`: Task description
    -   `completed`: Boolean status indicating if the task is completed

### User Management Service

-   **Create and retrieve users**
-   Each user includes:
    -   `id`: Unique identifier
    -   `username`: Unique username
    -   `email`: User email
-   **Mock task retrieval for a user**: Retrieve tasks associated with a specific user ID.

## Project Structure



`project/
├── task_service/           # Task Management Service
│   ├── app.py              # Main application entry point
│   ├── models.py           # Task model and in-memory storage
│   ├── routes.py           # Task-related routes and validation
│   ├── requirements.txt    # Dependencies for task service
├── user_service/           # User Management Service
│   ├── app.py              # Main application entry point
│   ├── models.py           # User model and in-memory storage
│   ├── routes.py           # User-related routes and validation
│   ├── requirements.txt    # Dependencies for user service
└── README.md               # Project README
` 

## Requirements

-   Python 3.7+
-   Flask (for both services)

## Installation and Setup

1.  **Clone the repository**:
    

    
    `git clone https://github.com/yourusername/microservices_project.git
    cd microservices_project` 
    
2.  **Install dependencies** for each service:
    
    For **Task Management Service**:
    
  
    
    `cd task_service
    pip install -r requirements.txt` 
    
    For **User Management Service**:
    

    
    `cd ../user_service
    pip install -r requirements.txt` 
    

## Running the Services

1.  **Run Task Management Service** (on port 5000):
    
 
    
    `cd task_service
    python app.py` 
    
2.  **Run User Management Service** (on port 5001):
    

    
    `cd ../user_service
    python app.py` 
    
    The services will run on:
    
    -   Task Management Service: `http://127.0.0.1:5000`
    -   User Management Service: `http://127.0.0.1:5001`

## Endpoints

### Task Management Service (http://127.0.0.1:5000)

-   **GET /tasks**: Retrieve all tasks.
-   **GET /tasks/<id>**: Retrieve a specific task by ID.
-   **POST /tasks**: Create a new task.
    -   **Request Body**:
        
        json
        

        
        `{
          "title": "Task title",
          "description": "Task description"
        }` 
        
-   **PATCH /tasks/<id>**: Update a specific task by ID.
    -   **Request Body**: Any of `title`, `description`, or `completed`.

### User Management Service (http://127.0.0.1:5001)

-   **GET /users**: Retrieve all users.
-   **POST /users**: Create a new user.
    -   **Request Body**:
        
        json
        

        
        `{
          "username": "johndoe",
          "email": "johndoe@example.com"
        }` 
        
-   **GET /users/<id>/tasks**: Retrieve tasks assigned to a user by ID (returns tasks from tasks service).

## Assumptions

-   Both services use in-memory storage (Python lists), so data is lost when services restart.
-   Each service runs independently on a different port and can be scaled separately.

## Future Improvements

-   **Data Persistence**: Replace in-memory storage with a database (e.g., SQLite, PostgreSQL) for data persistence.
-   **Inter-service Communication**: Modify the `GET /users/<id>/tasks` endpoint in the User Management Service to fetch actual task data from the Task Management Service.
-   **Error Handling and Logging**: Implement robust error handling and structured logging.
-   **Validation**: Move to a schema-based validation (e.g., using Marshmallow for both services) to improve input validation.
