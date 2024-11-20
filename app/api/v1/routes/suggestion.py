from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas.analysis import AnalysisSchema, ClothingAnalysisSchema
from app.api.v1.schemas.error import ServiceError
from app.db.base import get_db
from app.core.security import get_current_user 
from app.db.entity import User  
from app.services.suggestion_service import (
    get_last_suggestion,
    post_single_clothing_analysis
)

router = APIRouter()

@router.get("/get_last_suggestion/{item_id}", response_model=AnalysisSchema)
def get_last_suggestion_item( 
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    try:
        item = get_last_suggestion(db, item_id, int(current_user.id))
        return item
    except ServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/suggest_item/{clothing_id1}",response_model = ClothingAnalysisSchema)
async def suggest_item(clothing_id1: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_single_clothing_analysis(db, int(current_user.id), clothing_id1)
    
    