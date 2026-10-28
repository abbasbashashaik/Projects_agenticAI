from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from db.connection import get_db,Session
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, status
from models.user import User

router = APIRouter(prefix="/auth",tags=["Authorization"])

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str


class UserLogin(BaseModel):
  email_or_username: str
  password: str


class UserResponse(BaseModel):
  id: int
  username: str
  email: str
  created_at: datetime

  class Config:
    from_attributes = True  # Allows SQLAlchemy model conversion

# --- REGISTRATION ENDPOINT ---
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
  # Check if user already exists
  existing_user = (
      db.query(User)
      .filter(
          (User.email == user_data.email)
          | (User.username == user_data.username)
      )
      .first()
  )
  if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username or email already registered",
    )

  # Create new user instance (plain text password)
  new_user = User(
      username=user_data.username,
      email=user_data.email,
      password=user_data.password,
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


# --- LOGIN ENDPOINT ---
@router.post("/login")
def authenticate_user(login_data: UserLogin, db: Session = Depends(get_db)):
  # 1. Find the user by email or username
  user = (
      db.query(User)
      .filter(
          (User.email == login_data.email_or_username)
          | (User.username == login_data.email_or_username)
      )
      .first()
  )

  # 2. Check if user exists
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials (user not found)",
    )

  # 3. Direct string comparison for password
  if user.password != login_data.password:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials (incorrect password)",
    )

  # 4. Authentication successful
  return {
      "message": "Login successful",
      "user": {"id": user.id, "username": user.username, "email": user.email},
  }