from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class UserMessage(BaseModel):
    role: str = "user"
    query: str
    timestamp: datetime = Field(default_factory=datetime.now)

class Panel(BaseModel):
    text: str
    prompt: str
    image_url: str

class BotMessage(BaseModel):
    role: str = "bot"
    response: str
    storyboard: Optional[List[Panel]] = []
    timestamp: datetime = Field(default_factory=datetime.now)

class MessageLog(BaseModel):
    user: Optional[UserMessage] = None
    bot: Optional[BotMessage] = None

class Thread(BaseModel):
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "New Visualizer Story"
    messages: List[MessageLog] = [] 
    created_at: datetime = Field(default_factory=datetime.now)
