from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class Gender(str, Enum):
    """Enumeration for gender options"""
    male = "male"
    female = "female"

class Role(str, Enum):
    """Enumeration for user roles"""
    admin = "admin"
    user = "user"
    student = "student"

class User(BaseModel):
    """
    User model representing a complete user entity
    
    Attributes:
        id: Unique identifier for the user
        first_name: User's first name
        last_name: User's last name
        middle_name: Optional middle name
        gender: User's gender (male/female)
        roles: List of roles assigned to the user
    """
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Gender
    roles: List[Role]

class UserLogin(BaseModel):
    """
    Model for login credentials
    
    Attributes:
        username: User's login username
        password: User's password
    """
    username: str
    password: str

class UserUpdateRequest(BaseModel):
    """
    Model for user update requests
    Allows partial updates (all fields optional)
    
    Attributes:
        first_name: New first name (optional)
        last_name: New last name (optional)
        middle_name: New middle name (optional)
        gender: New gender (optional)
        roles: New roles list (optional)
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[Gender] = None
    roles: Optional[List[Role]] = None

