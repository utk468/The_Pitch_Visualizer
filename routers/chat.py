from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from backend.graph import pitch_graph
from backend.state import PitchState
from backend.database import db_manager
from schema.user import UserDetails
from schema.chat import MessageLog, UserMessage, BotMessage, Panel
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str 
    style: Optional[str] = "digital_art"
    user_id: Optional[str] = None 

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        initial_state: PitchState = {
            "narrative": request.message,
            "style": request.style,
            "segments": [],
            "prompts": [],
            "image_urls": [],
            "storyboard": [],
            "error": ""
        }

        result = await pitch_graph.ainvoke(initial_state)
        
        if result.get("error"):
            raise Exception(result["error"])

        if request.user_id:
            user_msg = UserMessage(query=request.message)
            wrapped_user_msg = MessageLog(user=user_msg)
            await db_manager.add_message_to_thread(request.user_id, request.thread_id, wrapped_user_msg)

            storyboard_panels = [
                Panel(text=p["text"], prompt=p["prompt"], image_url=p["image_url"])
                for p in result["storyboard"]
            ]
            
            bot_msg = BotMessage(
                response="Here is your visual storyboard:",
                storyboard=storyboard_panels
            )
            wrapped_bot_msg = MessageLog(bot=bot_msg)
            await db_manager.add_message_to_thread(request.user_id, request.thread_id, wrapped_bot_msg)

        return {
            "response": "Success",
            "storyboard": result["storyboard"]
        }

    except Exception as e:
        print(f"Error in Pitch reasoning: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
