from pydantic import BaseModel, Field

# Define a model for Todo items
class Todo(BaseModel):
    """
    Model representing a Todo item.

    Attributes:
    - title (str): Title of the Todo item.
    - description (str): Description of the Todo item.
    - completed (bool): Completion status of the Todo item.
    """
    title: str
    description: str
    completed: bool
