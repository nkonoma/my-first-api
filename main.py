from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models import User, Gender, Role, UserLogin, UserUpdateRequest
from typing import List
from uuid import UUID, uuid4
from auth import create_access_token
from middleware import AuthMiddleware

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Add authentication middleware
app.add_middleware(AuthMiddleware)

db: List[User] = [
    User(
        id=UUID("d11a058e-429c-479d-9fc6-96474181d5d1"), 
        first_name = "Nicolas",
        last_name = "Konoma",
        gender = Gender.male,
        roles = [Role.admin, Role.user]
        ),
    User(
        id=UUID("960677ed-5810-4853-a70c-c75532627d21"), 
        first_name = "John",
        last_name = "Doe",
        gender = Gender.male,
        roles = [Role.student]
        )
]

@app.get("/")
async def read_root(): # root endpoint
    return {"message": "Hello World. My name is Nic"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(user_credentials: UserLogin):
    """
    Authenticate user and return JWT token
    Args:
        user_credentials: Username and password
    Returns:
        dict: Access token and token type
    """
    if user_credentials.username == "admin" and user_credentials.password == "password":
        token = create_access_token(data={"sub": user_credentials.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """Serve the users list page"""
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/add-user", response_class=HTMLResponse)
async def add_user_page(request: Request):
    """Serve the add user page"""
    return templates.TemplateResponse("add_user.html", {"request": request})

@app.get("/edit-users", response_class=HTMLResponse)
async def edit_users_page(request: Request):
    """Serve the edit users page"""
    return templates.TemplateResponse("edit_users.html", {"request": request})

@app.get("/manage-users", response_class=HTMLResponse)
async def manage_users_page(request: Request):
    """Serve the delete users page"""
    return templates.TemplateResponse("delete_users.html", {"request": request})

# API Endpoints

@app.get("/api/v1/users")
async def fetch_users():
    """
    Get all users from database
    Returns:
        list: List of users
    """
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    """
    Create a new user
    Args:
        user: User data
    Returns:
        dict: Created user's ID
    """
    db.append(user)
    return {"id": user.id}

@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    """
    Update an existing user
    Args:
        user_id: UUID of user to update
        user_update: Updated user data
    Returns:
        User: Updated user object
    """
    for user in db:
        if user.id == user_id:
            # Update only provided fields
            for field, value in user_update.dict(exclude_unset=True).items():
                setattr(user, field, value)
            return user
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist")

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    """
    Delete a user
    Args:
        user_id: UUID of user to delete
    Returns:
        dict: Success message
    """
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist")
