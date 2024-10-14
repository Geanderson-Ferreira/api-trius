from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from typing import Optional
from datetime import date
from src.ohip_profiles import create_profile
from src.credentials import Credentials

ROTA = "/create-profile/"


# Inicializa o roteador de clientes
router = APIRouter()

class CustomerProfile(BaseModel):
    full_name: str
    citizen_country: constr(min_length=2, max_length=2)  # type: ignore # código do país com 2 caracteres
    date_of_birth: date  # agora é do tipo date
    email: EmailStr
    telephone: str
    residence_country: constr(min_length=2, max_length=2)  # type: ignore # código do país com 2 caracteres
    zip_code: str
    street: str
    residence_number: Optional[str]
    neighborhood: str
    complement: Optional[str]
    city: str
    state: constr(min_length=2, max_length=2)  # type: ignore # código do estado com 2 caracteres
    cpf: constr(min_length=11, max_length=11)  # type: ignore # CPF com 11 caracteres
    gender: Optional[str]

# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(hotel, profile: CustomerProfile, token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        credenciais = Credentials(hotel)

        p = create_profile(credenciais, profile.full_name, profile.citizen_country, profile.date_of_birth,
                       profile.email, profile.telephone, profile.residence_country,
                       profile.zip_code, profile.street, profile.residence_number,
                       profile.neighborhood, profile.complement, profile.city, profile.state,
                       profile.cpf, profile.gender)

        return {"profileIdCreated": p}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
