# Event Manager App API Project
This is a Python-based RESTful API with FastAPI that provides information for a Event Manager App.
It uses FastAPI, pydantic and sqlalchemy for integration with a relational database(sqlite).

## Running 
1. Clone repository.
2. pip install requirements.txt
3. Create a new .env file at the base of the project with these values:
	SECRET_KEY="Generate a random 32-byte (256-bit) secret key"
	ALGORITHM=HS256
4. Start server by running uvicorn main:app 

## API Documentation
Swagger UI documentation at [http://localhost:8000/docs/](http://localhost:8000/docs/) to interactively explore and test the API endpoints.

## Endpoints
- **user**
- **GET /api/v1/users/:** Retrieve a list of all users.
- **POST /api/v1/users/:** Add a new user.
- **POST /api/v1/users/role:** Add a new role.
- **GET /api/v1/users/me:** Read details for the current user.
- **POST /api/v1/users/token:** Log in a user and generate an access token.
- **GET /api/v1/users/roles:** Retrieve a list of roles.
- **DELETE /api/v1/users/{user_id}:** Delete a specific user.
- **event**
- **GET /api/v1/events/:** Retrieve a list of all events.
- **POST /api/v1/events/:** Add a new event.
- **POST /api/v1/events/status:** Add a new status.
- **GET /api/v1/events/status:** Retrieve a list of statuses.
- **POST /api/v1/events/attend/{event_id}:** Add the current user to an event.
- **PUT /api/v1/events/{event_id}:** Update an event.
- **DELETE /api/v1/events/{event_id}:** Delete an event.
- **PATCH /api/v1/events/{event_id}/status/{status_id}:** Change an event status.
- **GET /api/v1/events/status/{status_id}:** Retrieve a list of events by status.
