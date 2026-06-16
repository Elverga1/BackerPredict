from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from ventas import router as ventas_router
from produccion import router as produccion_router
from reportes import router as reportes_router
from usuarios import router as usuarios_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(ventas_router)
app.include_router(produccion_router)
app.include_router(reportes_router)
app.include_router(usuarios_router)
