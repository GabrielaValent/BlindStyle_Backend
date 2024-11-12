from sqlite3 import Timestamp
from pydantic import BaseModel, Field
from typing import Optional


class Description(BaseModel):
    description: str
    imageBase64: Optional[str] = None
    
    class Config:
        from_attributes = True
