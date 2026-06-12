from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Venta, ProduccionDiaria
from auth import obtener_usuario_actual

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.get("/resumen")
def obtener_reporte(db: Session = Depends(get_db),
            usuario_actual: str = Depends(obtener_usuario_actual)):
    
    total_pan_sal_vendido = (db.query(func.sum(Venta.pan_sal_vendido)).scalar() or 0)
    total_pan_dulce_vendido = (db.query(func.sum(Venta.pan_dulce_vendido)).scalar() or 0)
    ingresos_totales = (db.query(func.sum(Venta.ingreso_total)).scalar() or 0)
    total_pan_sal_producido = (db.query(func.sum(ProduccionDiaria.pan_sal_producido)).scalar() or 0)
    total_pan_dulce_producido = (db.query(func.sum(ProduccionDiaria.pan_dulce_producido)).scalar() or 0)
    total_pan_sal_sobrante = (db.query(func.sum(ProduccionDiaria.pan_sal_sobrante)).scalar() or 0)
    total_pan_dulce_sobrante = (db.query(func.sum(ProduccionDiaria.pan_dulce_sobrante)).scalar() or 0)

    return {
        "total_pan_sal_vendido": total_pan_sal_vendido,
        "total_pan_dulce_vendido": total_pan_dulce_vendido,
        "ingresos_totales": ingresos_totales,
        "total_pan_sal_producido": total_pan_sal_producido,
        "total_pan_dulce_producido": total_pan_dulce_producido,
        "total_pan_sal_sobrante": total_pan_sal_sobrante,
        "total_pan_dulce_sobrante": total_pan_dulce_sobrante
    }
    
    
    