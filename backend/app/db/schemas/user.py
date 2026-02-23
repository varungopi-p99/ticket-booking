from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr | None = None
    password: str
    retype_password: str

class UserLogin(BaseModel):
    email:str
    password: str

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse