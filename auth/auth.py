from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from config.database import user_collection
#///

SECRET_KEY = "JF4tT8aYmmw2vq9KuMWHmdRK"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')


def authenticate(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = user_collection.find_one({"user_name": payload.get('sub')})
        
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail="User Not Authenticated")

def create_access_token(data: dict, expires_date: timedelta = None):
    to_encode = data.copy()
    if expires_date:
        expire = datetime.now() + expires_date
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
    


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


