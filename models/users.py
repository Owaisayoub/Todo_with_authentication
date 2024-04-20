from pydantic import BaseModel

class User(BaseModel):
    user_name: str
    hashed_password: str 