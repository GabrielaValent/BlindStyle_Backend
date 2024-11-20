from typing import Optional
from pydantic import BaseModel

class ClothingAnalysisSchema(BaseModel):
    id : int
    clothing_id1 : int
    clothing_id2 : Optional[int]
    analysis_id : int
    
    class Config:
        from_attributes = True

class AnalysisSchema(BaseModel):
    analysis: str = ""
    
    class Config:
        from_attributes = True