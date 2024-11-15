from fastapi import FastAPI
from app.database import init_db 
from .routes import user_routes as user,posts_routes as posts , auth_routes as auth, comments_routes as comment


app = FastAPI()

app.include_router(user.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(comment.router)


@app.on_event("startup")
def startup_event():
    init_db()