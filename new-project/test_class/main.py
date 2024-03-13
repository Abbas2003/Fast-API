from fastapi import FastAPI,Path
from enum import Enum

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

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/")
def read_root():
    return {"Hello": "Fast API"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/get-student/{student_id}")
def get_student(student_id: int ):
    return students[student_id]