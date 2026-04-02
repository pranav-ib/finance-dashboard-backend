from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, record
from app.routers import users, records

app = FastAPI(title="Financial Dashboard")


Base.metadata.create_all(bind = engine)

app.include_router(users.router)
app.include_router(records.router)

@app.get("/")
def root():
    return{"message" :"Finance API is running"}


