from sqlalchemy.orm import Session
from app.api.v1.schemas.error import ServiceError
from app.api.v1.schemas.user import UserDto
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.db.entity import User as UserEntity

def create_user(db: Session, user: UserDto):
    
    new_user = UserEntity(
        name = user.name,
        username = user.username,
        password = user.password
    )
    
    db_user = db.query(UserEntity).filter(UserEntity.username == user.username).first()
    if db_user:
        raise ServiceError("Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = UserEntity(name=user.name, username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def login_jwt(db: Session, user: str):
    
    db_user = db.query(UserEntity).filter(UserEntity.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise ServiceError("Incorrect username or password")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}