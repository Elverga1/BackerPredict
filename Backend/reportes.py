from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Venta, ProduccionDiaria
from auth import obtener_usuario_actual
from models import Venta, ProduccionDiaria, ClimaHistorico

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
    
@router.get("/completo")
def reporte_completo(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    ventas = db.query(Venta).all()

    resultado = []

    for venta in ventas:
        produccion = db.query(ProduccionDiaria).filter(
            ProduccionDiaria.fecha == venta.fecha
        ).first()

        clima = db.query(ClimaHistorico).filter(
            ClimaHistorico.fecha == venta.fecha
        ).first()

        resultado.append({
            "fecha": venta.fecha,
            "pan_sal_vendido": venta.pan_sal_vendido,
            "pan_dulce_vendido": venta.pan_dulce_vendido,
            "ingreso_total": venta.ingreso_total,

            "pan_sal_producido": produccion.pan_sal_producido if produccion else 0,
            "pan_dulce_producido": produccion.pan_dulce_producido if produccion else 0,
            "pan_sal_sobrante": produccion.pan_sal_sobrante if produccion else 0,
            "pan_dulce_sobrante": produccion.pan_dulce_sobrante if produccion else 0,

            "temperatura": clima.temperatura if clima else None,
            "humedad": clima.humedad if clima else None,
            "lluvia": clima.lluvia if clima else None,
            "descripcion_clima": clima.descripcion if clima else "Sin registro"
        })

    return resultado
    