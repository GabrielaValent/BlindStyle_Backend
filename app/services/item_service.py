import base64
from datetime import datetime
from sqlalchemy.orm import Session
from app.api.v1.schemas.error import ServiceError
from app.db.entity import ClothingItem as ClothingItemEntity 
from app.api.v1.schemas.item import ClothingItemSchema, ClothingItemUpdateSchema, CompleteClothingItemSchema


def get_clothing_item(db: Session, item_id: int, user_id: int):
    dbReturn = db.query(ClothingItemEntity).filter(ClothingItemEntity.id == item_id, ClothingItemEntity.user_id == user_id).first()

    if not dbReturn:
        raise ServiceError("Item not found")
    
    item = item_entity_to_schema(dbReturn)
    return item

def item_entity_to_schema(item: ClothingItemEntity):
    image_url = base64.b64encode(item.image_url).decode('utf-8') if item.image_url else None
    new_item = CompleteClothingItemSchema(
        id = item.id,
        name = item.name,
        description = item.description,
        ownership = item.ownership,
        created_at = item.created_at,
        status = item.status,
        image_url = image_url
    )
    return new_item

def get_all_clothing_items(db: Session, user_id: int):
    dbReturn = db.query(ClothingItemEntity).filter(ClothingItemEntity.user_id == user_id).all()
    
    if not dbReturn:
        raise ServiceError("Items not found")
    
    return [item_entity_to_schema(item) for item in dbReturn]

def delete_clothing_item(db: Session, item_id: int, user_id: int):
    item = db.query(ClothingItemEntity).filter(ClothingItemEntity.id == item_id, ClothingItemEntity.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted"}
    
    raise ServiceError("Item not found")

def update_clothing_item_status(db: Session, item_id: int, item_update: ClothingItemUpdateSchema, user_id: int):
    item = db.query(ClothingItemEntity).filter(ClothingItemEntity.id == item_id, ClothingItemEntity.user_id == user_id).first()
    
    if not item:
        raise ServiceError("Item not found")
    item.status = item_update.status

    db.commit()
    db.refresh(item)
    return ClothingItemSchema(
        id = item.id,
        name = item.name,
        status = item.status,
        created_at = item.created_at
    )

def create_clothing_item(db: Session, item: ClothingItemSchema, user_id: int):
    image_url = base64.b64decode(item.image_url)
    new_item = ClothingItemEntity(
        user_id=user_id,
        name=item.name,
        description=item.description,
        ownership=item.ownership,
        image_url=image_url,
        created_at=datetime.now(),
        status = True
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return item