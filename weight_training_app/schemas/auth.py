from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    user_type: str | None = None

class Login(BaseModel):
    email: str
    password: str