# Blog Project Learn

A learning project that documents my journey from building a **command-line (CLI) blog management system** to developing a **REST API** using FastAPI and PostgreSQL.

The goal of this project is not just to build a blog application, but to learn backend development concepts such as database design, authentication, testing, Docker, and CI/CD through a real project.

---

## ✨ Features

* User management
* Create blog posts
* Add comments to posts
* View users
* View posts
* JWT Authentication
* Database migrations with Alembic
* Automated API testing with Pytest
* Dockerized development environment

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy ORM**
* **Psycopg**
* **Alembic**
* **Pytest**
* **Docker**
* **GitHub Actions** (CI)

---

## 📁 Project Structure

```text
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
│   ├── test_users.py
│   └── test_posts.py
│
├── alembic/
│   └── env.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/blog_project_learn.git
cd blog_project_learn
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file from `.env.example` and add your database credentials and secret key.

### Run the application

```bash
python app/main.py
```

or start the FastAPI server:

```bash
fastapi dev app/endpoint.py
```

---

## 🧪 Running Tests

```bash
python -m pytest
```

---

## 🐳 Docker

Build the image:

```bash
docker build -t blog-api .
```

Run with Docker Compose:

```bash
docker compose up
```

---

## 📚 Learning Goals

This project is being used to learn and practice:

* REST API development
* SQLAlchemy ORM
* Database migrations
* Authentication with JWT
* Dependency Injection
* Testing with Pytest
* Docker and Docker Compose
* GitHub Actions CI
* Backend project structure and best practices

---

## 📌 Status

🚧 This project is actively being developed as I continue learning backend engineering.
