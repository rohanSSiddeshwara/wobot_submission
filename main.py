from fastapi import FastAPI, Header, HTTPException

from pydantic import BaseModel
from starlette.responses import JSONResponse
import jwt
from bson import ObjectId
import credentials
from database import get_database
from models import Todo
from auth import authenticate




app = FastAPI()
todos = get_database()


# Function to get the token from the header
def get_token_from_header(x_token: str = Header(None)):
    if x_token:# If the token is present in the header
        return x_token
    else:
        raise HTTPException(status_code=400, detail="X-Token header not found")

# Function to validate the token
def validate_token(token):
    try:# If the token is valid
        jwt.decode(token, "secret_key", algorithms=["HS256"])
        return True
    except:
        return False



@app.post("/login")# Endpoint to login and get the token
def login(username: str, password: str):
    if username == credentials.username and password == credentials.password:
        # If the username and password match the predefined credentials then return the token
        return {"access_token": jwt.encode({"username": username}, "secret_key", algorithm="HS256")}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/todos")# Endpoint to create a new task in the database
def create_todo(todo: Todo, x_token: str = Header(None)):
    # If the token is valid then create a new task in the database
    token = get_token_from_header(x_token)
    if validate_token(token):# If the token is valid
        result = todos.insert_one(todo.dict())# Insert the task in the database
        return {"task_id": str(result.inserted_id)}# Return the task id
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

@app.get("/todos/{task_id}")# Endpoint to get a task from the database
def read_todo(task_id: str, x_token: str = Header(None)):#
    token = get_token_from_header(x_token)
    if validate_token(token):
        todo = todos.find_one({"_id": ObjectId(task_id)})# Find the task in the database
        if todo:
            todo["_id"] = str(todo["_id"])# Convert the task id to string
            return todo # Return the task
        else:
            raise HTTPException(status_code=400, detail="Task not found")
    else:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.put("/todos/{task_id}")# Endpoint to update a task in the database
def update_todo(task_id: str, todo: Todo, x_token: str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        todos.update_one({"_id": ObjectId(task_id)}, {"$set": todo.dict()})# Update the task in the database
        return {"task_id": task_id}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

@app.delete("/todos/{task_id}")# Endpoint to delete a task from the database
def delete_todo(task_id: str, x_token:str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        todos.delete_one({"_id": ObjectId(task_id)}) # Delete the task from the database
        return {"task_id": task_id}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")
