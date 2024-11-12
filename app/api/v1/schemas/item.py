from datetime import datetime
from sqlite3 import Timestamp
from pydantic import BaseModel
from typing import Optional

class ClothingItemUpdateSchema(BaseModel):
    status: bool = True


class ClothingItemSchema(BaseModel):
    name: str
    description: Optional[str] = None
    ownership: Optional[bool] = True
    image_url: Optional[str] = None
    created_at: Optional[Timestamp]
    status: bool = True
    
    class Config:
        from_attributes = True


class CompleteClothingItemSchema(BaseModel):
    id: int
    name: str
    description: str
    ownership: bool
    created_at: datetime
    status: bool = True
    image_url: str
    
    class Config:
        from_attributes = True