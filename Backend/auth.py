from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_db
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse, LoginRequest, Token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "clave_secreta_temporal" #Cambia la clave secreta, depende del equipo(pc)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hashear_password(password: str):
    return pwd_context.hash(password[:72])

def verificar_password(password: str, password_hash: str):
    return pwd_context.verify(password[:72], password_hash)

def crear_token(data: dict):
    datos = data.copy()

    expiracion = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos.update({"exp": expiracion})

    token = jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

@router.post("/register", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.nombre == usuario.nombre).first()

    if usuario_db:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        password_hash=hashear_password(usuario.password),
        rol="admin"
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

@router.post("/login", response_model=Token)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(
        Usuario.nombre == datos.nombre
    ).first()

    if not usuario_db:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    if not verificar_password(datos.password, usuario_db.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = crear_token(
        data={"sub": usuario_db.nombre}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }