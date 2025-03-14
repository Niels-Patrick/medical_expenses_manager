from fastapi import FastAPI
from modules import routes, routes_user

app = FastAPI()

app.include_router(routes_user.router, prefix="/users", tags=["Users"])
app.include_router(routes.router, prefix="/patients", tags=["Patients"])
