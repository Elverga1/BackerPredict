from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models import ProduccionDiaria, Venta
from schemas import ProduccionCreate, ProduccionResponse
from auth import obtener_usuario_actual

router = APIRouter(
    prefix="/produccion",
    tags=["Produccion"]
)

@router.post("/", response_model=ProduccionResponse)
def registrar_produccion(
    produccion: ProduccionCreate,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    venta = db.query(Venta).filter(
        Venta.fecha == produccion.fecha
    ).first()

    pan_sal_vendido = 0
    pan_dulce_vendido = 0

    if venta:
        pan_sal_vendido = venta.pan_sal_vendido
        pan_dulce_vendido = venta.pan_dulce_vendido

    pan_sal_sobrante = produccion.pan_sal_producido - pan_sal_vendido
    pan_dulce_sobrante = produccion.pan_dulce_producido - pan_dulce_vendido

    produccion_existente = db.query(ProduccionDiaria).filter(
        ProduccionDiaria.fecha == produccion.fecha
    ).first()

    if produccion_existente:
        produccion_existente.pan_sal_producido = produccion.pan_sal_producido
        produccion_existente.pan_dulce_producido = produccion.pan_dulce_producido
        produccion_existente.pan_sal_vendido = pan_sal_vendido
        produccion_existente.pan_dulce_vendido = pan_dulce_vendido
        produccion_existente.pan_sal_sobrante = pan_sal_sobrante
        produccion_existente.pan_dulce_sobrante = pan_dulce_sobrante

        db.commit()
        db.refresh(produccion_existente)

        return produccion_existente
    
    nueva_produccion = ProduccionDiaria(
        fecha = produccion.fecha,
        pan_sal_producido = produccion.pan_sal_producido,
        pan_dulce_producido = produccion.pan_dulce_producido,
        pan_sal_vendido = pan_sal_vendido,
        pan_dulce_vendido = pan_dulce_vendido,
        pan_sal_sobrante = pan_sal_sobrante,
        pan_dulce_sobrante = pan_dulce_sobrante
    )

    db.add(nueva_produccion)
    db.commit()
    db.refresh(nueva_produccion)

    return nueva_produccion

@router.get("/", response_model=list[ProduccionResponse])
def listar_produccion(db: Session = Depends(get_db), 
            usuario_actual: str = Depends(obtener_usuario_actual)):
    producciones = db.query(ProduccionDiaria).all()
    return producciones

@router.get("/{fecha}", response_model=ProduccionResponse)
def obtener_produccion(fecha: date, db: Session = Depends(get_db),
            usuario_actual: str = Depends(obtener_usuario_actual)):
    produccion = db.query(ProduccionDiaria).filter(
        ProduccionDiaria.fecha == fecha
    ).first()

    if not produccion:
        raise HTTPException(
            status_code=404,
            detail= "No existe producción para esa fecha"
        )

    return produccion