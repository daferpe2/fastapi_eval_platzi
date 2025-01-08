from fastapi import FastAPI,Depends
from typing import Annotated
from sqlmodel import Session,create_engine,SQLModel

sqlite_name = "reportes.db"
sql_url = f"sqlite:///./{sqlite_name}"

enigine = create_engine(sql_url)

def create_tables_db(app:FastAPI):
    SQLModel.metadata.create_all(enigine)
    yield

def get_session():
    with Session(enigine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]