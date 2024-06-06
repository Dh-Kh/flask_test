# Flask Ticket System

## Overview

This project is a web application developed using Flask that implements a simple ticket system with different user roles and groups. The application features a simple authentication mechanism and Role Based Access Control (RBAC) to manage user permissions and access.

## Features

### Ticket Properties

- **Status**:
  - Pending
  - In Review
  - Closed
- **User or Group Assignment**
- **Note**: A simple text field for additional information

### User Roles

- **Admin**:
  - Can manage all groups and tickets.
- **Manager**:
  - Assigned to a specific group.
  - Can manage only tickets from their assigned group.
- **Analyst**:
  - Assigned to a specific group.
  - Can work only with tickets from their assigned group.

### User Groups

- Customer 1
- Customer 2
- Customer 3

## Project Structure (tree -I 'venv|__pycache__|migrations|files*')
.
├── app
│   ├── app_admin.py
│   ├── app_rbac.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── commands.py
│   ├── extensions.py
│   ├── __init__.py
│   ├── models
│   │   ├── tickets.py
│   │   └── users.py
│   ├── rbac
│   │   ├── __init__.py
│   │   └── models.py
│   └── templates
│       └── auth
│           └── login.html
├── config.py
├── Dockerfile
├── manage.py
└── requirements.txt

### Prerequisites

* **Docker:** Make sure Docker and Docker Compose are installed on your system.

### Setup

1. **Clone the Repository:**
```bash
   git clone https://github.com/Dh-Kh/flask_test.git
   cd backend
```

2. **Execute commands:**
```bash
   docker-compose build 
   docker-compose up -d
   docker-compose run backend flask db init
   docker-compose run backend flask db migrate -m "Initial migration."
   docker-compose run backend flask db upgrade
   docker-compose run backend flask generate_roles
   docker-compose run backend flask generate_groups
   docker-compose run backend flask generate_user_groups 50
   docker-compose run backend flask generate_tickets 100
   docker-compose run backend python3 manage.py
```

3. **Urls** 
- /login
- /admin
- /admin/logout

4. **Warning**
```bash
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.28.0.3:8000
```
- use second url not localhost