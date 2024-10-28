# fastapi_neon/main.py

from fastapi import FastAPI, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from typing import Annotated

ALGORITHM = "HS256"
SECRET_KEY = "A Secure Sec222ret Key"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-endpoint")

fake_users_db: dict[str, dict[str, str]] = {
    "ameenalam": {
        "username": "ameenalam",
        "full_name": "Ameen Alam",
        "email": "ameenalam@example.com",
        "password": "ameenalamsecret",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "mjunaidsecret",
    },
    "mabbas": {
        "username": "mjunaid",
        "full_name": "Mohammad Abbas",
        "email": "mabbas@example.com",
        "password": "mabbassecret",
    },
}

def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI(title="Hello World API", version="0.0.1")

@app.post("/login-endpoint")
def login_request(data_from_user: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm )]):

    # Step 1: username Exist in DB - Else error
    user_in_fake_db = fake_users_db.get(data_from_user.username)
    if user_in_fake_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    # Step 2: Check password - Else error
    if user_in_fake_db["password"] != data_from_user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Step 2: Generate Token
    access_token_expires = timedelta(minutes=1)
    generated_token = create_access_token(subject=data_from_user.username, expires_delta=access_token_expires)  


    return {"username": data_from_user.username,
            "access_token": generated_token}

@app.get("/all-users")
def get_all_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return fake_users_db

@app.get("/special-items")
def get_special_items(token: Annotated[str, Depends(oauth2_scheme)]):
    # Decode Token
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return {"special": "items", "token": token, "decoded_data": decoded_data
    }

@app.get("/")
def read_root():
    return {"Hello": "Dev container"}

@app.get("/container")
def read_root2():
    return {"content": "Docker Container"}   

@app.get("/new_route")
def get_access_token(user_name: str):

    access_token_expires = timedelta(minutes=1)
    print("access_token_expires", access_token_expires)

    access_token = create_access_token(subject=user_name, expires_delta=access_token_expires)  

    return {"access_token": access_token}


def decode_access_token(token: str):
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_data

@app.get("/decode-token")
def decode_token(token: str):
    try:
        decoded_data = decode_access_token(token)
        return decoded_data
    except JWTError as e:
        return {"error": str(e)}