from fastapi import FastAPI
from fastapi.openapi.models import SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from app.database import init_db
from .routes import user_routes as user, posts_routes as posts, auth_routes as auth, comments_routes as comment

app = FastAPI()

# Include your routers
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(comment.router)


@app.on_event("startup")
def startup_event():
    init_db()

# Customize OpenAPI to use Bearer token authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
