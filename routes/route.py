from fastapi import Response, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId

from models.todos import Todo
from config.database import todo_collection, user_collection
from auth.auth import *

router = APIRouter()

@router.get('/todo/', response_model=dict)
async def get_todos(response: Response, token: str = Depends(oauth2_scheme)):
    """
    Retrieve all todos for the authenticated user.

    Parameters:
    - response (Response): FastAPI response object.
    - token (str, optional): Authorization token. Defaults to Depends(oauth2_scheme).

    Returns:
    - dict: Dictionary containing the status and data of the todos.

    Raises:
    - HTTPException: If authentication fails or there's an issue with retrieving todos.
    """
    try:
        user = authenticate(token)
        user_id = str(user["_id"])
        todos = []
        todos_objects = todo_collection.find({"user_id": user_id})
    
        for todo in todos_objects:
            todo["_id"] = str(todo["_id"])
            del todo["user_id"]
            todos.append(todo)
        
        return {
            'status': "success",
            "data": todos
        }
    except HTTPException as e:
        response.status_code = e.status_code
        return {
            "status": "fail",
            "status_code": e.status_code,
            "data": e.detail
        }

@router.get('/todo/{id}', response_model=dict)
async def get_todo(id: str, response: Response, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a specific todo for the authenticated user by its ID.

    Parameters:
    - id (str): ID of the todo to retrieve.
    - response (Response): FastAPI response object.
    - token (str, optional): Authorization token. Defaults to Depends(oauth2_scheme).

    Returns:
    - dict: Dictionary containing the status and data of the todo.

    Raises:
    - HTTPException: If authentication fails or the todo with the specified ID is not found.
    """
    try:
        user = authenticate(token)
        user_id = str(user["_id"])
        todo = todo_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
        if not todo:
            raise HTTPException(status_code=404, detail="Todo doesn't exist")
        todo["_id"] = str(todo["_id"])
        del todo["user_id"]
        return {
            'message': "success",
            "data": todo
        }
    except HTTPException as e:
        response.status_code = e.status_code
        return {
            "status": "fail",
            "status_code": e.status_code,
            "data": e.detail
        }

@router.post('/todo/', response_model=dict)
async def post_todo(todo: Todo, response: Response, token: str = Depends(oauth2_scheme)):
    """
    Create a new todo for the authenticated user.

    Parameters:
    - todo (Todo): Todo model object containing todo details.
    - response (Response): FastAPI response object.
    - token (str, optional): Authorization token. Defaults to Depends(oauth2_scheme).

    Returns:
    - dict: Dictionary containing the status and data of the created todo.

    Raises:
    - HTTPException: If authentication fails or there's an issue with creating the todo.
    """
    try:
        user = authenticate(token)
           
        data = dict(todo)
        data["user_id"] = str(user["_id"])
        created_todo_id = todo_collection.insert_one(data).inserted_id
        
        if not created_todo_id:
            raise HTTPException(status_code=500, detail="Internal server error")
        
        res = todo_collection.find_one({"_id": created_todo_id})
        res["_id"] = str(res["_id"])
        del res["user_id"]

        response.status_code = 201

        return {
                'Status': "Success",
                "data": res
            }
    
    except HTTPException as e:
        response.status_code = e.status_code
        return {
            "status": "Fail",
            "status_code": e.status_code,
            "data": e.detail
        }

@router.patch('/todo/{id}', response_model=dict)
async def update_todo(id: str, response: Response, todo: Todo, token: str = Depends(oauth2_scheme)):
    """
    Update a specific todo for the authenticated user by its ID.

    Parameters:
    - id (str): ID of the todo to update.
    - response (Response): FastAPI response object.
    - todo (Todo): Todo model object containing updated todo details.
    - token (str, optional): Authorization token. Defaults to Depends(oauth2_scheme).

    Returns:
    - dict: Dictionary containing the status and data of the updated todo.

    Raises:
    - HTTPException: If authentication fails, the todo with the specified ID is not found, or there's an issue with updating the todo.
    """
    try:
        user = authenticate(token)
        user_id = str(user["_id"])

        updated_todo = todo_collection.find_one_and_update({"_id": ObjectId(id), "user_id": user_id}, {"$set": dict(todo)})
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Not Found")
        
        updated_todo["_id"] = str(updated_todo["_id"])
        del updated_todo["user_id"]

        return {
            "status": "Success",
            "data": updated_todo
        }
    except HTTPException as e:
        response.status_code = e.status_code
        return {
            "status": "Fail",
            "status_code": e.status_code,
            "data": e.detail
        }

@router.delete('/todo/{id}')
async def delete_todo(id: str, response: Response, token: str = Depends(oauth2_scheme)):
    """
    Delete a specific todo for the authenticated user by its ID.

    Parameters:
    - id (str): ID of the todo to delete.
    - response (Response): FastAPI response object.
    - token (str, optional): Authorization token. Defaults to Depends(oauth2_scheme).

    Returns:
    - dict: Dictionary containing the status of the deletion operation.

    Raises:
    - HTTPException: If authentication fails, or the todo with the specified ID is not found.
    """
    try:
        user = authenticate(token)
        user_id = str(user["_id"])
    
        result = todo_collection.find_one_and_delete({"_id": ObjectId(id), "user_id": user_id})
        if not result:
            raise HTTPException(status_code=404, detail="Todo Not found")
        response.status_code = 204
        return {
            "status": "Success",
            "data": None
        }
    except HTTPException as e:
        response.status_code = e.status_code
        return {
            "status": "Fail",
            "status_code": e.status_code,
            "data": e.detail
        }

@router.post('/signup')
async def sign_up(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Register a new user.

    Parameters:
    - form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
    - dict: Dictionary containing the access token for the registered user.

    Raises:
    - HTTPException: If the provided username already exists.
    """
    user_name= form_data.username
    password = form_data.password

    user = user_collection.find_one({"user_name": user_name})
    if user:
        raise HTTPException(status_code=400, detail="User already exist")

    hased_password = pwd_context.hash(password)
    saved_user = user_collection.insert_one({"user_name": user_name, "hased_password": hased_password})
    res = user_collection.find_one({"_id": saved_user.inserted_id})
    res["_id"] = str(res["_id"])
    del res["_id"]

    access_token = create_access_token(data= {"sub": user_name})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login for existing users.

    Parameters:
    - form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
    - dict: Dictionary containing the access token for the authenticated user.

    Raises:
    - HTTPException: If the provided username or password is invalid.
    """
    user_name = form_data.username
    password = form_data.password

    user = user_collection.find_one({"user_name": user_name})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username or password")

    if not verify_password(password, user["hased_password"]):
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    access_token = create_access_token(data= {"sub": user_name})
    return {"access_token": access_token, "token_type": "bearer"}
