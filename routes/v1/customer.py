from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY

ROTA = "/customer-profile/"


# Inicializa o roteador de clientes
router = APIRouter()

# Modelo de perfil de cliente
class CustomerProfile(BaseModel):
    name: str
    birth_date: str  # Pode usar datetime.date se quiser validar datas
    email: str

# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(profile: CustomerProfile, token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Imprime o perfil do cliente no terminal
        print(f"Received customer profile: Name: {profile.name}, Birth Date: {profile.birth_date}, Email: {profile.email}")

        return {"message": "Customer profile received successfully"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
