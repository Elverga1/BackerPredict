from fastapi import FastAPI
from auth import router as auth_router
from ventas import router as ventas_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(ventas_router)
@app.get("/")
def Prueba():
    return {"message": "Bienvenido a la API de autenticación"}