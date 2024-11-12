from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.error import ServiceError
from app.core.security import generate_token_from_refresh
from app.db.base import get_db
from app.api.v1.schemas.user import UserDto, TokenDto
from app.services.user_service import create_user, login_jwt 

router = APIRouter()

@router.post("/register_user", response_model=UserDto)
def register_user(
    user: UserDto, 
    db: Session = Depends(get_db)
):
    try:
        return create_user(db, user)
    
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenDto)
def login(
    user: UserDto, 
    db: Session = Depends(get_db)
):
    try:
        return login_jwt(db, user)
    
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh_token", response_model=TokenDto)
def update_expired_token(
    refresh_token: str 
):
    try:
        return generate_token_from_refresh(refresh_token)
    
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))

