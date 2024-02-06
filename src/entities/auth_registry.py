from pydantic import BaseModel

class AuthRegistry(BaseModel):
    userId: str
    email: str
    password: str
    fullName: str