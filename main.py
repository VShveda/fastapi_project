from fastapi import FastAPI

from user import routes


app = FastAPI()

app.include_router(routes.router, prefix="/api/user", tags=["User API"])
