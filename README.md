# User Management System

A FastAPI-based user management system with MySQL database integration.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```sql
CREATE DATABASE dbname;
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dbname.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

4. Create a `.env` file in the root directory:
```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=dbname
```

5. Run the server:
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
