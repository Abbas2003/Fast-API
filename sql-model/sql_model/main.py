from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated

from sql_model import settings


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    age: int | None = None

class HeroCreate(HeroBase):
    age: int | None = None

class HeroResponse(HeroBase):
    id: int
    age: int | None = None


connectionString = str(settings.DB_URL).replace("postgresql", "postgresql+psycopg2")

engine = create_engine(connectionString, echo=True, pool_recycle=600)

def create_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Create Database..")
    create_tables()
    yield
    
app = FastAPI(lifespan=lifespan)

# DB Dependency Injection
def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
async def root():
    return {"Message": "Learning SQLModel"}

# Get all Heroes
@app.get("/heroes", response_model=list[Hero])
def get_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    return heroes
    
# Create Heroes
@app.post("/heroes", response_model=HeroResponse)
def create_hero(hero: HeroCreate, db: Annotated[Session, Depends(get_session)]):
    
    print("DATA FROM CLIENT:",hero)
    hero_to_insert = Hero.model_validate(hero)
    print("DATA AFTER VALIDATION:", hero_to_insert)

    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert