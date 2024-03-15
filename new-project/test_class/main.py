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

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/")
def read_root():
    return {"Hello": "Fast API"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/get-student/{student_id}")
# def get_student(student_id: int ):
#     return students[student_id]

# Query Parameters
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz1"},
    {"item_name": "Baz2"},
    {"item_name": "Baz3"},
    {"item_name": "Baz4"},
    {"item_name": "Baz5"},
    {"item_name": "Baz6"},
    {"item_name": "Baz7"},
    {"item_name": "Baz8"},
    ]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# @app.get("/items")
# async def get_items(q: str | None=None):
#     message = {"message": "This is a by-default message"}
#     if q:
#         message.update({"message": q})
#     return message

@app.get("/items/{item_id}")
async def get_item_id(item_id: int, q: str | None=None, short: bool=False):
    message = {"item_id": item_id}
    if q:
        message.update({"q": q})
    if not short:
        message.update(
            {"description": "This is a good item"}
        )
    return message