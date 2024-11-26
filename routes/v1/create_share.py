from fastapi import APIRouter, Depends, HTTPException
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from src.ohip_profiles import create_profile
from src.credentials import Credentials
from models.models import GuestProfile
from src.ohip_reservations import create_share

ROTA = "/create-share/"


# Inicializa o roteador de clientes
router = APIRouter()


# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(hotel, reservationIdParent: int, shareProfileId, token: str = Depends(oauth2_scheme)):

    """
    Rota cria o compartilhamento de um quarto.

    """
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
 
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    credenciais = Credentials(hotel)

    result = create_share(credentials=credenciais, resv_id_parent=reservationIdParent, share_profile_id=shareProfileId)

    return result

    if profile_criado['status'] == 200:
        return profile_criado['content']
    else:
        raise HTTPException(status_code=401, detail=profile_criado['content'])
