from fastapi import FastAPI
from modules import routes, routes_user, routes_ai
import logging

logging.basicConfig(filename='medical_expenses_manager.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.include_router(routes_user.router, prefix="/users", tags=["Users"])
app.include_router(routes.router, prefix="/patients", tags=["Patients"])
app.include_router(routes_ai.router, prefix="/AI", tags=["AI"])
