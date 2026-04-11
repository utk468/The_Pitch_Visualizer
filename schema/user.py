from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from .chat import Thread

class UserDetails(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = "Anonymous"
    email: str 
    hashed_password: str
    # here adding list of threads for users
    threads: List[Thread] = [] 
    created_at: datetime = Field(default_factory=datetime.now)
