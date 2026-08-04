# blog_project_learn
Documenting the journey of me making a blog management system (CLI) -> REST APIs

## Features
- Can create users
- make posts
- add comments
- display users
- view post

## Tech Stack
Python
PostgreSQL
SQLalchemy ORM
FastAPI
Psycopg
Alembic
Pytest
docker

## Project structure
blog_project_learn/
│
├── app/
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   ├── menu.py
│   ├── main.py
│   ├── endpoint.py
│   ├── security.py
│   └── dependencies.py
│ 
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_endpoints.py
│   ├── tests_users.py
│   └── test_posts.py
│
│ 
├── alembic/
│   └── env.py
│
├── alembic.ini
│
├── requirements.txt
│
├── Dockerfile
│
├── docker-compose.yml
│
└── README.md
