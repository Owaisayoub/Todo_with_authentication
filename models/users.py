from pydantic import BaseModel

# Define a model for User
class User(BaseModel):
    """
    Model representing a User.

    Attributes:
    - user_name (str): Username of the user.
    - hashed_password (str): Hashed password of the user.
    """
    user_name: str
    hashed_password: str
