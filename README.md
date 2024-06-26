# FastAPI Todo App

This is a simple FastAPI application that allows users to manage their todo items. Users can create, read, update, and delete todo items. Authentication is required to access the todo endpoints.

## Endpoints

### Todo Endpoints

1. **POST /todo/**

   - Create a new todo item.
   - Requires authentication with an access token.

2. **GET /todo/**

   - Get all todo items.
   - Requires authentication with an access token.

3. **GET /todo/{id}**

   - Get a specific todo item by ID.
   - Requires authentication with an access token.

4. **PATCH /todo/{id}**

   - Update a specific todo item by ID.
   - Requires authentication with an access token.

5. **DELETE /todo/{id}**
   - Delete a specific todo item by ID.
   - Requires authentication with an access token.

### Authentication Endpoints

1. **POST /login/**

   - Authenticate a user and obtain an access token.
   - Requires providing username and password.

2. **POST /signup/**
   - Create a new user account.
   - Requires providing username, and password.

## Authentication

- Authentication for accessing todo endpoints is done using OAuth2 token-based authentication.
- To access todo endpoints, clients must obtain an access token by authenticating via the `/login/` endpoint.
- Users can create a new account using the `/signup/` endpoint.
- The access token obtained after login/signup must be included in the `Authorization` header of requests to todo endpoints.

## Environment Variables

This project uses the following environment variables:

- **SECRET_KEY**: Used for encryption and security purposes.
- **DATABASE_URL**: URL of the database used by the application.

Make sure to set these environment variables before running the application. You can customize their values according to your environment.

## How to Run

1. Install Python (if not already installed).
2. Clone this repository.
3. Navigate to the project directory.
4. Create a virtual environment: `python -m venv venv`.
5. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`.
7. Run the FastAPI server: `uvicorn main:app --reload`.
8. Access the API at `http://localhost:8000`.

## API Documentation

- The API documentation (Swagger UI) is available at `http://localhost:8000/docs`.
- You can explore and test the API endpoints using the Swagger UI.
- You can also you postman(personal favorite)

## Author

- **Owais Ayoub Ganaie**
