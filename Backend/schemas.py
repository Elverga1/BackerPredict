from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal

class UsuarioCreate(BaseModel):
    nombre: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    rol: str
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    nombre: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class VentaCreate(BaseModel):
    fecha: date
    pan_sal_vendido: int
    pan_dulce_vendido: int

class VentaResponse(BaseModel):
    id: int
    fecha: date
    pan_sal_vendido: int
    pan_dulce_vendido: int
    ingreso_total: Decimal
    fecha_registro: datetime

    class Config:
        from_attributes = True

class ProduccionCreate(BaseModel):
    fecha: date
    pan_sal_producido: int
    pan_dulce_producido: int

class ProduccionResponse(BaseModel):
    id: int
    fecha: date
    pan_sal_producido: int
    pan_dulce_producido: int
    pan_sal_vendido: int
    pan_dulce_vendido: int
    pan_sal_sobrante: int
    pan_dulce_sobrante: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

class ClimaResponse(BaseModel):
    id: int
    fecha: date
    temperatura: Decimal
    humedad: int
    lluvia: bool
    descripcion: str
    fecha_registro: datetime

    class Config:
        from_attributes = True