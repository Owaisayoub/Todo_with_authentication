from pydantic import BaseModel,Field


#create a model by inheriting the BaseModel

class Todo(BaseModel):
    
    # id: str 
    title: str
    description: str
    completed: bool
    # user_id: str = Field(..., title="User ID", description="The ID of the user who created the todo")

# class UserTodo(BaseModel):
#     title: str
#     description: str
#     completed: bool
#     # user_id: str