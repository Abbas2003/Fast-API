from fastapi.testclient import TestClient
from prac_todo import settings
from sqlmodel import SQLModel, create_engine, Session, select, Field
from prac_todo.main import get_session, app, Todos


def test_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Welcome To Todo App!"}

def test_write_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=600)
    
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override
        
        client = TestClient(app=app)
        todo_content = "Eating Biryani"
        
        response = client.post("/todos", 
                    json={"content": todo_content})
        
        data = response.json()
        assert response.status_code == 200
        assert data["content"] == todo_content

def test_read_list_main():
    connection_string = str(settings.TEST_DB_URL).replace(
        "postgresql", "postgresql+psycopg2"
    )
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=600)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)

        response = client.get("/todos")
        data = response.json()
        assert response.status_code == 200

def test_update_main():
    connection_string = str(settings.TEST_DB_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=600)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        todo_content = "Eating Biryani"
        response = client.put("/todos/32",
                    json={"content": todo_content,
                    "status": True})
        data = response.json()
        assert response.status_code == 200
        assert data["content"] == todo_content

def test_delete_main():
    connection_string = str(settings.TEST_DB_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=600)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        todo_content = "Eating Biryani"
        response = client.delete("/todos/32")
        data = response.json()
        assert response.status_code == 200
        assert data["content"] == todo_content