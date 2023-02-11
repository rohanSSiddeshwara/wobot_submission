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



def get_token_from_header(x_token: str = Header(None)):
    if x_token:
        return x_token
    else:
        raise HTTPException(status_code=400, detail="X-Token header not found")

def validate_token(token):
    try:
        jwt.decode(token, "secret_key", algorithms=["HS256"])
        return True
    except:
        return False


@app.post("/login")
def login(username: str, password: str):
    if username == credentials.username and password == credentials.password:
        return {"access_token": jwt.encode({"username": username}, "secret_key", algorithm="HS256")}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/todos")
def create_todo(todo: Todo, x_token: str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        result = todos.insert_one(todo.dict())
        return {"task_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

@app.get("/todos/{task_id}")
def read_todo(task_id: str, x_token: str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        todo = todos.find_one({"_id": ObjectId(task_id)})
        if todo:
            todo["_id"] = str(todo["_id"])
            return todo
        else:
            raise HTTPException(status_code=400, detail="Task not found")
    else:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.put("/todos/{task_id}")
def update_todo(task_id: str, todo: Todo, x_token: str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        todos.update_one({"_id": ObjectId(task_id)}, {"$set": todo.dict()})
        return {"task_id": task_id}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

@app.delete("/todos/{task_id}")
def delete_todo(task_id: str, x_token:str = Header(None)):
    token = get_token_from_header(x_token)
    if validate_token(token):
        todos.delete_one({"_id": ObjectId(task_id)})
        return {"task_id": task_id}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")
