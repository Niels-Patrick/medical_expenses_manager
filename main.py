from fastapi import FastAPI
from modules import routes
from modules.database import engine

app = FastAPI()

app.include_router(routes.router)
