from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from backend.graph import triage_graph
from backend.state import TriageState
from backend.database import db_manager
from schema.user import UserDetails
from schema.chat import MessageLog
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str 
    history: List[str] = []
    user_name: Optional[str] = "Anonymous"
    user_email: Optional[str] = "None"
    user_id: Optional[str] = None 

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 1. Initialize Graph State
        initial_state: TriageState = {
            "query": request.message,
            "history": request.history,
            "intent": "",
            "symptoms": [],
            "risk_level": "Normal",
            "final_response": ""
        }

        # 2. Run the reasoning engine
        result = await run_in_threadpool(triage_graph.invoke, initial_state)
        
        # 3. --- Persistence Logic (Nested Threads) ---
        if request.user_id:
            from schema.chat import UserMessage, BotMessage, MessageLog
            
            # Save User Message
            user_msg = UserMessage(query=request.message)
            wrapped_user_msg = MessageLog(user=user_msg)
            await db_manager.add_message_to_thread(request.user_id, request.thread_id, wrapped_user_msg)

            # Save Bot Response
            bot_msg = BotMessage(
                response=result["final_response"],
                symptoms=result["symptoms"],
                risk_level=result["risk_level"]
            )
            wrapped_bot_msg = MessageLog(bot=bot_msg)
            await db_manager.add_message_to_thread(request.user_id, request.thread_id, wrapped_bot_msg)

        return {
            "response": result["final_response"],
            "intent": result["intent"],
            "symptoms": result["symptoms"],
            "risk_level": result["risk_level"]
        }

    except Exception as e:
        print(f"Error in triage reasoning: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
