from fastapi import FastAPI, HTTPException, Depends
from models import User, Gender, Role, UserUpdateRequest, UserLogin
from typing import List
from uuid import UUID
from auth import security, create_access_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()
security = HTTPBearer()

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

@app.post("/login")
async def login(user_credentials: dict):
 # In a real app, verify credentials against a database
    if user_credentials.get("username") == "admin" and user_credentials.get("password") == "password":
        token = create_access_token(
            data={"sub": user_credentials["username"]}
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password"
    )

@app.get("/api/v1/users") # get all users
async def fetch_users(token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return db;

@app.post("/api/v1/users")
async def register_user(user: User, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message" : "User was successfully deleted"}
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exist"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db: # loop through the users in the database
        if user.id == user_id: # if the user id is the same as the user id in the database
            if user_update.first_name is not None: # if the first name is not None
                user.first_name = user_update.first_name # update the first name
            if user_update.last_name is not None: # if the last name is not None
                user.last_name = user_update.last_name # update the last name
            if user_update.middle_name is not None: # if the middle name is not None
                user.middle_name = user_update.middle_name # update the middle name
            if user_update.gender is not None: # if the gender is not None
                user.gender = user_update.gender # update the gender
            if user_update.roles is not None: # if the roles is not None
                user.roles = user_update.roles # update the roles
            return {"message": "User was successfully updated"}
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exist"
    )
