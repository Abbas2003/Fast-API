from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session, select
from prac_todo import settings


class Todos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    todo: str = Field(index=True)
    is_complete: bool = Field(default=False)


connectionString = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg2")

engine = create_engine(connectionString, echo=True, connect_args={"sslmode": "require"}, pool_recycle=600)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Create database...")
    create_db_and_table()
    yield 



app = FastAPI(
    title="Todo App",
    lifespan=life_span,
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "DELETE", "PUT"],
#     allow_headers=["*"],
# )

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
async def root():
    return {"Greetings": "Welcome To Todo App!"}    

@app.post("/todos/",response_model=Todos)
def add_todos(todo: Todos, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos",response_model=list[Todos])
def get_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todos)).all()
    return todos

@app.delete("/todos/{todo_id}", response_model=Todos)
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(Todos).where(Todos.id == todo_id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return todo


class updateTodo():
    status: bool

@app.put("/todos/{todo_id}", response_model=Todos)
def update_todo(todo_id: int, todo: Todos, session: Annotated[Session, Depends(get_session)]):
    todo_query = session.exec(select(Todos).where(Todos.id == todo_id)).first()
    if not todo_query:
        raise HTTPException(status_code=404, detail="Todos not found")
    todo_query.status = todo.is_complete
    session.commit()
    session.refresh(todo_query)
    return todo_query