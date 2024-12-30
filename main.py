from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import User, UserCreate, UserLogin, UserResponse, UserUpdateRequest, Base, Gender
from security import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Datsumb8@localhost/new_schema"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create initial admin user if it doesn't exist
def create_test_user():
    db = SessionLocal()
    # Check if admin user already exists
    if not db.query(User).filter(User.username == "admin").first():
        # Create admin user
        admin_user = User(
            first_name="Admin",
            last_name="User",
            gender=Gender.Male,
            username="admin",
            password=hash_password("password")  # Hash the password!
        )
        db.add(admin_user)
        db.commit()
    db.close()

# Create database tables and admin user
Base.metadata.create_all(bind=engine)
create_test_user()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Handle user login"""
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create new user
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        username=user.username,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdateRequest, db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    if user_update.first_name is not None:
        db_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        db_user.last_name = user_update.last_name
    if user_update.gender is not None:
        db_user.gender = user_update.gender
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
