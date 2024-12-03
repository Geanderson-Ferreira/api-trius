from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from typing import Optional
from datetime import date
from src.ohip_profiles import create_or_update_profile
from src.credentials import Credentials
from models.models import GuestProfile

ROTA = "/update-profile/{profileId}"


def update_profile(p):
    print(p)

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
async def update_customer_profile(hotel: str, profileId: str, profile: GuestProfile, token: str = Depends(oauth2_scheme)):
    # # Decodifica o token para verificar a autenticidade
    # payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # username = payload.get("sub")
    # if username is None:
    #     raise HTTPException(status_code=401, detail="Invalid token")

    credenciais = Credentials(hotel)

    profile_criado = create_or_update_profile(credenciais, profile.fullName, profile.citizenCountry, profile.dateOfBirth,
                profile.email, profile.telephone, profile.residenceCountry,
                profile.zipCode, profile.street, profile.residenceNumber,
                profile.neighborhood, profile.complement, profile.city, profile.state,
                profile.cpfOrPassport, profile.gender, prof_id=profileId)
    
    if profile_criado['status'] == 200:
        return profile_criado['content']
    else:
        raise HTTPException(status_code=401, detail=profile_criado['content'])
    