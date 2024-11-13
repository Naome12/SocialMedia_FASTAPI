from fastapi import FastAPI
from app.models import Users, Posts, Comments   # Import Base from Users.py
from app.database import engine,init_db 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Social Media API"}

# Database initialization
@app.on_event("startup")
async def startup_event():
   await init_db()






