from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: Optional[str] = None # first name of the user
    last_name: Optional[str] = None # last name of the user 
    middle_name: Optional[str] = None # middle name of the user
    gender: Optional[Gender] = None # gender of the user
    roles: list[Role] = Optional[list[Role]] # roles of the user

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None # first name of the user
    last_name: Optional[str] = None # last name of the user 
    middle_name: Optional[str] = None # middle name of the user
    gender: Optional[Gender] = None # gender of the user
    roles: list[Role] = Optional[list[Role]] # roles of the user

class UserLogin(BaseModel):
    username: str
    password: str

