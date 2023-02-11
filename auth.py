import jwt
import credentials
from fastapi import Header, HTTPException



def authenticate(username: str, password: str):
    if username == credentials.username and password == credentials.password:
        return {"access_token": jwt.encode({"username": username}, "secret_key", algorithm="HS256")}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

