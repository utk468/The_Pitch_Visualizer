from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
import uuid

class UserMessage(BaseModel):
    role: str = "user"
    query: str
    timestamp: datetime = Field(default_factory=datetime.now)

class BotMessage(BaseModel):
    role: str = "bot"
    response: str
    symptoms: Optional[List[str]] = []
    risk_level: Optional[str] = "Normal"
    timestamp: datetime = Field(default_factory=datetime.now)

class MessageLog(BaseModel):
    
    user: Optional[UserMessage] = None
    bot: Optional[BotMessage] = None

    role: Optional[str] = None 
    content: Optional[str] = None
    query: Optional[str] = None
    response: Optional[str] = None
    symptoms: Optional[List[str]] = None
    risk_level: Optional[str] = None
    timestamp: Optional[datetime] = None

class Thread(BaseModel):
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "New Conversation"
    messages: List[MessageLog] = [] 
    created_at: datetime = Field(default_factory=datetime.now)
