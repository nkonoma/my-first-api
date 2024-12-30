from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from enum import Enum as PyEnum
from typing import Optional

Base = declarative_base()

# Simple enums
class Gender(str, PyEnum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

# Just one simple table to start
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # For hashed password

# Pydantic models for API
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    gender: Gender
    username: str

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None

    model_config = ConfigDict(from_attributes=True)

