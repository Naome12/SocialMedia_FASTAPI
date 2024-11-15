from fastapi import FastAPI
from app.models import Users, Posts, Comments   # Import Base from Users.py
from app.database import init_db  # We only need init_db, not the engine anymore
from .routes import user_routes


app = FastAPI()

# Include the user routes under the /users path
app.include_router(user_routes.router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to the Social Media API"}

# Database initialization
@app.on_event("startup")
def startup_event():
    # Call the sync init_db function to create tables
    init_db()
