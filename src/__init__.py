from fastapi import  FastAPI,status
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from fastapi.responses import JSONResponse
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from .middleware import register_middleware
from .errors import(
   InvalidToken,
RevokedToken,
AccessTokenRequired,
RefreshTokenRequired,
UserAlreadyExists,
InvalidCredentials,
InsufficientPermission,
BookNotFound,
TagNotFound,
TagAlreadyExists,
UserNotFound,create_exception_handler
)
@asynccontextmanager
async def life_span(app:FastAPI):
   await init_db()
   yield 
   print(f"server has been stopped")

version = "v1"
app= FastAPI(
    title="bookly",
version = version,
description="A rest api for book review web service ",
lifespan=life_span 
)
register_middleware(app)
def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Tag Already exists",
                "error_code": "tag_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"]) #add this
app.include_router(book_router, prefix = f"/api/{version}/books")
app.include_router(auth_router, prefix = f"/api/{version}/auth")
"""What is REST?

REST stands for Representational State Transfer.
It is a set of rules/architecture style used for communication between:

Client → frontend/mobile/browser
Server → backend/database/API server

REST is mainly used on the web using HTTP.

Intuitive Understanding

Think of a restaurant.

Customer → Client
Kitchen → Server
Menu → API
Waiter carrying requests/responses → HTTP

You ask:

“Give me details of burger #5”

The waiter takes the request to kitchen and brings response.

That is basically REST API communication.

What is an API?

API = Application Programming Interface

It is a way for two software systems to communicate.

Example:

Instagram frontend talks to Instagram backend using APIs.
Your React app talks to FastAPI backend using APIs.
Then What is REST API?

A REST API is an API that follows REST principles.

Example URL:

https://example.com/users/5

This represents:

resource = user
specific user id = 5

Server sends data usually in JSON.

Example response:

{
  "id": 5,
  "name": "Ravi",
  "age": 21
}
Main Idea of REST

REST treats everything as a resource.

Examples:

users
products
posts
comments

Each resource has a URL.

Example:

/users
/products
/orders
HTTP Methods in REST

These are VERY important.

Method	Purpose
GET	Read data
POST	Create data
PUT	Update entire data
PATCH	Update partial data
DELETE	Remove data
Example

Suppose we have a users database.

1. GET → Fetch users
GET /users

Response:

[
  {
    "id":1,
    "name":"Ravi"
  },
  {
    "id":2,
    "name":"Asha"
  }
]
2. GET specific user
GET /users/1

Response:

{
  "id":1,
  "name":"Ravi"
}
3. POST → Create user
POST /users

Body:

{
  "name":"Kiran"
}

Server creates user.

4. PUT → Replace user
PUT /users/1

Body:

{
  "name":"New Name"
}
5. DELETE → Delete user
DELETE /users/1
REST Principles

These are the core rules.

1. Client-Server Separation

Frontend and backend are separate.

React frontend can talk to:

FastAPI backend
Node backend
Django backend

independently.

2. Stateless

Server does NOT remember previous requests.

Every request must contain all needed information.

Example:

GET /profile
Authorization: Bearer token

Server checks token every time.

3. Resource-Based URLs

Good REST:

/users/5
/products/10

Bad REST:

/getUserById

REST prefers nouns/resources.

4. Uses Standard HTTP Methods

GET, POST, PUT, DELETE etc.

Why REST Became Popular

Because it is:

simple
scalable
language independent
frontend/backend independent
easy for web/mobile apps
REST API Flow
Frontend ----HTTP Request----> Backend API
Frontend <---JSON Response---- Backend API

Example:

React App ---> GET /users ---> FastAPI
React App <--- JSON users ---- FastAPI"""