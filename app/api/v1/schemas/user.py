from pydantic import BaseModel

class UserDto(BaseModel):
    name: str = None
    username: str
    password: str
    
    class Config:
        from_attributes = True

class TokenDto(BaseModel):
    access_token: str
    refresh_token: str = None


class DecodedTokenSchema(BaseModel):
        id: int