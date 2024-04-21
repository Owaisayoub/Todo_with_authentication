import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from config.database import user_collection

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')

def authenticate(token):
    """
    Authenticates the user by decoding the JWT token.

    Parameters:
    - token (str): JWT token to authenticate.

    Returns:
    - dict: User information if authentication is successful.

    Raises:
    - HTTPException: If authentication fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = user_collection.find_one({"user_name": payload.get('sub')})
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail="User Not Authenticated")

def create_access_token(data: dict, expires_date: timedelta = None):
    """
    Creates an access token using JWT.

    Parameters:
    - data (dict): Data to be encoded in the token.
    - expires_date (timedelta, optional): Expiry duration for the token. Defaults to 15 minutes.

    Returns:
    - str: Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_date:
        expire = datetime.now() + expires_date
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    """
    Verifies the given plain password against the hashed password.

    Parameters:
    - plain_password (str): Plain text password.
    - hashed_password (str): Hashed password to compare against.

    Returns:
    - bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
