from fastapi import FastAPI


app = FastAPI(title="FastAPI Auth")

@app.get("/")
def root():
    return {"message": "Fast API authentication"}