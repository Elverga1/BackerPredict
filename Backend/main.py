from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)
@app.get("/")
def Prueba():
    return {"message": "Bienvenido a la API de autenticación"}