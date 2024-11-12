from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas.error import ServiceError
from app.api.v1.schemas.user import UserDto
from app.db.base import get_db
from app.api.v1.schemas.item import ClothingItemSchema, ClothingItemUpdateSchema, CompleteClothingItemSchema
from app.core.security import get_current_user 
from app.db.entity import User  
from app.services.item_service import (
    create_clothing_item,
    get_clothing_item,
    get_all_clothing_items,
    delete_clothing_item,
    update_clothing_item_status,
)

router = APIRouter()


@router.get("/get_item/{item_id}", response_model=CompleteClothingItemSchema)
def read_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        item = get_clothing_item(db, item_id, int(current_user.id))
        return item
    except ServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get_item_list", response_model=list[CompleteClothingItemSchema])  
def read_all_items(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  
):
    try:
        return get_all_clothing_items(db, int(current_user.id))
    
    except ServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/delete_item/{item_id}", response_model=dict) 
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  
):
    try:
        delete_clothing_item(db, item_id, int(current_user.id))
        return {"message": "Item deleted successfully"}
    
    except ServiceError as e:
            raise HTTPException(status_code=404, detail=str(e))

@router.put("/update_item_status/{item_id}", response_model=ClothingItemSchema)  
def update_item(
    item_id: int, 
    item_update: ClothingItemUpdateSchema, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  
):
    try:
        return update_clothing_item_status(db, item_id, item_update, int(current_user.id))
    except ServiceError as e:
                raise HTTPException(status_code=404, detail=str(e))

@router.post("/create_item", response_model=ClothingItemSchema)  
def create_item_route(
    item: ClothingItemSchema, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> ClothingItemSchema:
    return create_clothing_item(db, item, current_user.id)