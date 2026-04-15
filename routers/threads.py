from fastapi import APIRouter, HTTPException, Depends
from typing import List
import os
import jwt
from backend.database import db_manager
from schema.chat import Thread
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid session")

@router.post("/")
async def create_thread(token: str):
    user_id = await get_current_user_id(token)
    new_thread = await db_manager.create_thread(user_id)
    return new_thread

@router.get("/")
async def list_threads(token: str):
    user_id = await get_current_user_id(token)
    threads = await db_manager.get_user_threads_summary(user_id)
    return threads

@router.delete("/{thread_id}")
async def delete_thread(thread_id: str, token: str):
    user_id = await get_current_user_id(token)
    await db_manager.delete_thread(user_id, thread_id)
    return {"status": "deleted"}

@router.get("/{thread_id}")
async def get_thread(thread_id: str, token: str):
    user_id = await get_current_user_id(token)
    thread = await db_manager.get_thread_by_id(user_id, thread_id)
    if thread:
        return thread
    raise HTTPException(status_code=404, detail="Thread not found")
