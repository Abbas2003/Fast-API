# fastapi_neon/main.py

from fastapi import FastAPI,Path

app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

students = {
    1: {
        "name": "Abbas",
        "age": 20,
        "class": "2 year CS",
    },
    2: {
        "name": "Aqsa",
        "age": "Pata Nhi",
        "class": "Mommy",
    },
    3: {
        "name": "Aftab",
        "age": "Main nh bataonga",
        "class": "Daddy",
    }
}


@app.get("/")
def read_root():
    return {"Hello": "Fast API"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/get-student/{student_id}")
def get_student(student_id: int ):
    return students[student_id]