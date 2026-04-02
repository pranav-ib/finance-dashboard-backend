from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, record

app = FastAPI(title="Financial Dashboard")

Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return{"message" :"Finance API is running"}


