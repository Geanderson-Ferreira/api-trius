from fastapi import APIRouter, Depends, HTTPException
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from src.ohip_profiles import create_profile
from src.credentials import Credentials
from models.models import GuestProfile
from src.ohip_reservations import create_share
from pydantic import BaseModel

ROTA = "/create-share/"

# Inicializa o roteador de clientes
router = APIRouter()

# Definindo o modelo que será utilizado no corpo da requisição
class ShareRequestBody(BaseModel):
    reservationIdParent: int
    shareProfileId: int

# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(
    body: ShareRequestBody,  # Agora os dados vêm no corpo
    hotel: str,               # Parâmetro adicional
    token: str = Depends(oauth2_scheme)
):
    """
    Rota cria o compartilhamento de um quarto.
    Recebe reservationIdParent, resv_id_parent e shareProfileId no corpo da requisição.
    """
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Extrair os dados do corpo da requisição
    reservationIdParent = body.reservationIdParent
    shareProfileId = body.shareProfileId

    print(reservationIdParent)
    print(shareProfileId)

    # Criar credenciais
    credenciais = Credentials(hotel)

    # Chama a função de criação de compartilhamento
    result = create_share(
        credentials=credenciais,
        resv_id_parent=reservationIdParent,
        share_profile_id=shareProfileId
    )

    # Verifica a resposta e retorna de acordo
    if result['status'] == 200:
        return result['content']
    else:
        raise HTTPException(status_code=401, detail=result['content'])
