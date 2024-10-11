from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme

# Inicializa o roteador de clientes
router = APIRouter()

# Simulação de banco de dados
fake_profiles = {
    1234: {"name": "João", "email": "joao@example.com", "birth_date": "1990-01-01"},
    5678: {"name": "Maria", "email": "maria@example.com", "birth_date": "1985-05-15"},
}

# Modelo de resposta
class ProfileResponse(BaseModel):
    id: int
    name: str

# Rota para obter o perfil pelo ID
@router.get("/customer-profile/{profile_id}", response_model=ProfileResponse)
async def get_customer_profile(profile_id: int, token: str = Depends(oauth2_scheme)):
    # Verifica se o token é válido (a lógica de validação pode ser mais complexa em produção)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Busca o perfil no "banco de dados"
    profile = fake_profiles.get(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"id": profile_id, "name": profile["name"]}
