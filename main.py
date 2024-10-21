from fastapi import FastAPI

from user import routes as user_routes
from posts import routes as posts_routes


app = FastAPI()

app.include_router(user_routes.router, prefix="/api/user", tags=["User API"])
app.include_router(posts_routes.router, prefix="/api/posts", tags=["Posts API"])
