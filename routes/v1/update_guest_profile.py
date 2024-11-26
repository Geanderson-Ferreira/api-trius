from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from typing import Optional
from datetime import date
from models.models import GuestProfile

ROTA = "/update-profile/"


# Inicializa o roteador de clientes
router = APIRouter()


# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(profile: GuestProfile, token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"profile": profile}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
