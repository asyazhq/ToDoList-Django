# A Simple RESTful API application for managing a task list (ToDo list) based on the Django (DRF) framework

This is a simple RESTful API for managing a ToDo list. The API allows users to create an account, authenticate, and manage their tasks. Users can create, update, delete, filter, and retrieve tasks.

## Features
- User registration, authentication and task management
- CRUD operations (Create, retrieve, update, and delete) for tasks
- Filtering tasks by status
- Task ownership restrictions
- Pagination support

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Setup
```bash
# Clone the repository
git clone <REPOSITORY_URL>
cd todo-list

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate    # For Windows

# Install dependencies
pip install -r requirements.txt

# Configure Database (PostgreSQL)
Update DATABASES in settings.py with your PostgreSQL credentials.

# Apply migrations
python manage.py migrate

# Start the server
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000/

## API Documentation

### Authentication
This API uses session-based authentication. Users must first log in to access protected endpoints.
- Register: `POST /api/v1/auth/register/`
- Login: `POST /api/v1/auth/login/` 
- Logout: `GET /api/v1/auth/logout/`

### User Endpoints

| Method       | Endpoint                              | Description         |
| ------------ | ------------------------------------- | ------------------- |
| GET          | /api/v1/users/                        | List all users      |
| GET          | /api/v1/users/{id}/                   | Get user details    |
| PUT          | /api/v1/users/{id}/                   | Update user profile |
| DELETE       | /api/v1/users/{id}/                   | Delete user account |

### Task Endpoints

| Method       | Endpoint                              | Description                    |
| ------------ | ------------------------------------- | ------------------------------ |
| GET          | /api/v1/tasks/                        | List all tasks of the user     |
| POST         | /api/v1/tasks/                        | Create a new task              |
| GET          | /api/v1/tasks/{id}/                   | Retrieve a specific task       |
| PUT          | /api/v1/tasks/{id}/                   | Update a task (Owner only)     |
| DELETE       | /api/v1/tasks/{id}/                   | Delete a task (Owner only)     |

### Additional Features

| Method       | Endpoint                              | Description                    |
| ------------ | ------------------------------------- | ------------------------------ |
| PATCH        | /api/v1/tasks/{id}/mark_completed/    | Mark task as completed         |
| GET          | /api/v1/tasks/?status=new             | Filter tasks by status         |
| GET          | /api/v1/tasks/?page=2                 | Pagination support             |

## Running Tests
To run unit tests:
```bash
python manage.py test
```

# Request examples

## Registration example

To register a new user just do the following request to the api:

Make a `post` request on the route `/api/v1/auth/register`

Header:
```
Content-Type: application/json
```

Body:
```json
{
  "username": "username",
  "first_name": "test",
  "last_name": "test",
  "password": "testpassword"
}

```
## Login example

The login (if succeed) will return you the things you can do once you are logged in (i.e: All the route you can access). Login will also provides 2 things inside the cookies:
- The session id used to determine your session
- The CSRF token to prevent Cross Site Request Forgery

Make a `post` request on the route `/api/v1/auth/login`

Header:
```
Content-Type: application/json
```

Body:
```json
{
  "username": "username",
  "first_name": "test",
  "last_name": "test",
  "password": "testpassword"
}
```

## Create a to do task

To create a to do task you first need to create a session by login to the API, then execute a `post` request on the following route: `/api/v1/tasks/`

Header
```
Content-Type: application/json
X-CSRFToken: <generated_token>
```
The generated CSRFT token will be found in the same place as the sessionid, which is inside the cookies.

Body
```json
{
    "title": "Finish project report",
    "description": "Complete and submit the final project report for the IT course"
}
```

## Video Demonstration
[The link to the video](https://youtu.be/fM3XZ4yrNf4)
