from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from models import Venta
from schemas import VentaCreate, VentaResponse

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

pan_precio = 5.00

@router.post("/", response_model=VentaResponse)
def registrar_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    ingreso_total = (venta.pan_sal_vendido + venta.pan_dulce_vendido) * pan_precio
    venta_existente = db.query(Venta).filter(Venta.fecha == venta.fecha).first()

    if venta_existente:
        venta_existente.pan_sal_vendido = venta.pan_sal_vendido
        venta_existente.pan_dulce_vendido = venta.pan_dulce_vendido
        venta_existente.ingreso_total = ingreso_total
        db.commit()
        db.refresh(venta_existente)
        return venta_existente
    
    nueva_venta = Venta(
        fecha = venta.fecha,
        pan_sal_vendido = venta.pan_sal_vendido,
        pan_dulce_vendido = venta.pan_dulce_vendido,
        ingreso_total = ingreso_total
    )

    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    return nueva_venta

@router.get("/", response_model=list[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    ventas = db.query(Venta).all()
    return ventas

@router.get("/{fecha}", response_model=VentaResponse)
def obtener_venta(fecha: date, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(
        Venta.fecha == fecha
    ).first()

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="No existe venta para esa fecha"
        )

    return venta