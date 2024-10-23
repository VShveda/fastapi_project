from fastapi import FastAPI

from user import routes as user_routes
from posts import routes as posts_routes
from comments import routes as comments_routes


app = FastAPI()

app.include_router(
    user_routes.router,
    prefix="/api/user",
    tags=["User API"]
)
app.include_router(
    posts_routes.router,
    prefix="/api/posts",
    tags=["Posts API"]
)
app.include_router(
    comments_routes.router,
    prefix="/api/comments",
    tags=["Comments API"]
)
