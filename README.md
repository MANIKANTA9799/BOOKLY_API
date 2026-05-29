# 📚 Bookly API

A production-style REST API built with **FastAPI** following modern backend engineering practices. It demonstrates authentication, authorization, database management, API design, and scalable backend architecture.

---

## 🚀 Features

### Authentication & Authorization

* JWT Authentication
* Access Tokens
* Refresh Tokens
* Secure Password Hashing
* Protected Routes
* Role-Based Access Control (RBAC)

### Books Management

* Create Books
* Retrieve Books
* Update Books
* Delete Books
* Search and Filter Books

### Reviews System

* Add Reviews
* Update Reviews
* Delete Reviews
* Associate Reviews with Books

### Tags System

* Create Tags
* Assign Tags to Books
* Organize Books by Categories

### Database Features

* PostgreSQL Integration
* SQLModel ORM
* Async Database Operations
* Alembic Migrations

### Backend Features

* Dependency Injection
* Custom Middleware
* Global Exception Handling
* Environment-Based Configuration
* OpenAPI Documentation
* Modular Architecture

---

## 🛠️ Tech Stack

| Category          | Technology |
| ----------------- | ---------- |
| Backend Framework | FastAPI    |
| Language          | Python     |
| Database          | PostgreSQL |
| ORM               | SQLModel   |
| Authentication    | JWT        |
| Password Hashing  | Passlib    |
| Migrations        | Alembic    |
| ASGI Server       | Uvicorn    |

---

## 📂 Project Structure

```text
BOOKLY_API/
│
├── migrations/
│
├── src/
│   ├── auth/
│   ├── books/
│   ├── db/
│   ├── reviews/
│   ├── tags/
│   ├── config.py
│   ├── errors.py
│   ├── middleware.py
│   └── __init__.py
│
├── alembic.ini
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/MANIKANTA9799/BOOKLY_API.git
cd BOOKLY_API
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=
```

---

## 🗄️ Database Migration

Create a migration:

```bash
alembic revision --autogenerate -m "initial migration"
```

Apply migrations:

```bash
alembic upgrade head
```

---

## ▶️ Running the Application

```bash
uvicorn src:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```


---

## 🏗️ Architecture Highlights

* Modular Domain-Based Structure
* Async FastAPI Endpoints
* JWT Authentication Flow
* Role-Based Access Control
* SQLModel ORM Integration
* Database Migration Management
* Custom Middleware Support
* Global Exception Handling

---

## 🎯 Learning Outcomes

This project helped me gain hands-on experience with:

* FastAPI
* SQLModel
* PostgreSQL
* Alembic
* JWT Authentication
* API Security
* Dependency Injection
* Middleware
* Error Handling
* Production-Oriented Backend Development

---

## 📜 License

This project is intended for educational and learning purposes.
