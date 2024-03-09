# fastapi_neon/main.py

from fastapi import FastAPI

app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

students = [
    1: {
        "name": "Abbas",
        "age": 20,
        "class": "2 year CS",
    }
]


@app.get("/")
def read_root():
    return {"Hello": "Fast API"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the student you want to view")):
    return students[student_id]