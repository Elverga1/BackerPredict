from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import requests

from database import get_db
from models import ClimaHistorico
from auth import obtener_usuario_actual

router = APIRouter(
    prefix="/clima",
    tags=["Clima"]
)


def obtener_descripcion(weather_code: int):
    codigos = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos fuertes",
        95: "Tormenta"
    }

    return codigos.get(weather_code, "Clima no identificado")


@router.get("/hoy")
def obtener_clima_hoy(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    fecha_hoy = date.today()

    clima_existente = db.query(ClimaHistorico).filter(
        ClimaHistorico.fecha == fecha_hoy
    ).first()

    if clima_existente:
        return clima_existente

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=18.9608"
        "&longitude=-99.5906"
        "&current=temperature_2m,relative_humidity_2m,rain,weather_code"
        "&timezone=America%2FMexico_City"
    )

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener el clima desde Open-Meteo"
        )

    if "current" not in datos:
        raise HTTPException(
            status_code=500,
            detail="La API de clima no devolvió datos actuales"
        )

    clima_actual = datos["current"]

    temperatura = clima_actual.get("temperature_2m")
    humedad = clima_actual.get("relative_humidity_2m")
    rain = clima_actual.get("rain", 0)
    weather_code = clima_actual.get("weather_code")

    if temperatura is None or humedad is None or weather_code is None:
        raise HTTPException(
            status_code=500,
            detail="Faltan datos de clima en la respuesta de Open-Meteo"
        )

    lluvia = rain > 0
    descripcion = obtener_descripcion(weather_code)

    nuevo_clima = ClimaHistorico(
        fecha=fecha_hoy,
        temperatura=temperatura,
        humedad=humedad,
        lluvia=lluvia,
        descripcion=descripcion
    )

    db.add(nuevo_clima)
    db.commit()
    db.refresh(nuevo_clima)

    return nuevo_clima

@router.get("/")
def listar_clima(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    climas = db.query(ClimaHistorico).all()
    return climas