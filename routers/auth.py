from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
import os
import datetime
import jwt
from passlib.context import CryptContext
from backend.database import db_manager
from schema.user import UserDetails
from schema.auth import UserLogin, UserRegister
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "temporary_secret_key_change_me_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 

def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(pwd_bytes.decode("utf-8", "ignore"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(pwd_bytes.decode("utf-8", "ignore"), hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@router.post("/register")
async def register(profile: UserRegister):
    await db_manager.connect()
    # Check if user already exists
    existing_user = await db_manager.db.users.find_one({"email": profile.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = UserDetails(
        name=profile.name,
        email=profile.email,
        hashed_password=hash_password(profile.password)
    )
    await db_manager.save_user(new_user)
    
    token = create_access_token({"sub": str(new_user.user_id), "email": new_user.email})
    return {"access_token": token, "token_type": "bearer", "user": {"name": new_user.name, "email": new_user.email, "id": new_user.user_id}}




@router.post("/login")
async def login(credentials: UserLogin):
    await db_manager.connect()
    user_data = await db_manager.db.users.find_one({"email": credentials.email})
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user_data["user_id"]), "email": user_data["email"]})
    return {"access_token": token, "token_type": "bearer", "user": {"name": user_data["name"], "email": user_data["email"], "id": user_data["user_id"]}}
