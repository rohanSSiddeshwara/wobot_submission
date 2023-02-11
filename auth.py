import jwt
import credentials
from fastapi import HTTPException

def authenticate(username: str, password: str):
    # Function to check if the provided username and password match the predefined credentials
    if username == credentials.username and password == credentials.password:
        return {"access_token": jwt.encode({"username": username}, "secret_key", algorithm="HS256")}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
