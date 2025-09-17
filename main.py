from fastapi import FastAPI

from api.routers.main_router import main_router
from api.routers.auth_router import auth_router

app = FastAPI()

app.include_router(main_router)
app.include_router(auth_router)
