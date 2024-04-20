from fastapi import Response, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId


from models.todos import Todo
from config.database import todo_collection, user_collection
from auth.auth import *


router = APIRouter()


@router.get('/todo/', response_model=dict)
async def get_todos(response: Response, token: str = Depends(oauth2_scheme)):
    try:
        user = authenticate(token)
        user_id = str(user["_id"])
        todos = []
        todos_objects = todo_collection.find({"user_id": user_id})
    
        for todo in todos_objects:
            todo["_id"] = str(todo["_id"])
            del todo["user_id"]
            # print(todo)
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
async def get_todo(id: str,response: Response, token: str= Depends(oauth2_scheme)):
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
async def update_todo(id: str,response: Response, todo: Todo, token: str = Depends(oauth2_scheme)):
    
    try:
        user = authenticate(token)
        user_id = str(user["_id"])
        # print(user_id)


        updated_todo = todo_collection.find_one_and_update({"_id": ObjectId(id), "user_id": user_id}, {"$set": dict(todo)})
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Not Found")
        
        updated_todo["_id"] = str(updated_todo["_id"])
        
        # res = dict(updated_todo)
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

        

@router.delete('/todo/{id}',)
async def delete_todo(id: str, response: Response, token: str = Depends(oauth2_scheme)):

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

    # return res
    access_token = create_access_token(data= {"sub": user_name})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_name = form_data.username
    password = form_data.password

    # we can create a validate password function in order to check if the user has entered valid password
    #validate_password()

    #get the user from the database 
    user = user_collection.find_one({"user_name": user_name})

    #raise the exception if the user correspoding to user_name provided doesn't exist or there is password mismatch
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    #To verify_password function we passed the plain password that user provided and hashed password which is in database for verificaton
    if not verify_password(password, user["hased_password"]):
        
        raise HTTPException(status_code=404, detail="Invalid username or password")
    

    #generate teh access token by passsing the sub as user_name
    access_token = create_access_token(data= {"sub": user_name})
    return {"access_token": access_token, "token_type": "bearer"}


    
