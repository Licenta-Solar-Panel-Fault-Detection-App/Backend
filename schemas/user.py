from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdateUsername(BaseModel):
    username: str

class UserUpdateEmail(BaseModel):
    email: str

class UserUpdatePassword(BaseModel):
    password: str

