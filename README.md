# My First API

A FastAPI-based REST API with user authentication.

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd my-first-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the server:
```bash
uvicorn main:app --reload
``` 
5. Visit API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

- POST /login - Login endpoint
- GET /api/v1/users - Get all users
- POST /api/v1/users - Create a new user
