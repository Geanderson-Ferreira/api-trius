from fastapi import APIRouter, Depends, HTTPException, Query
from src.credentials import Credentials
from typing import List
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from src.ohip_profiles import get_profiles

ROTA = "/get-profiles"


router = APIRouter()

@router.get(ROTA)
async def get_guest_profiles(
    hotelId: str, profileId: List[int] = Query(..., max_length=6), token: str = Depends(oauth2_scheme)
):
    """Obtém perfis de hóspedes com base nos parâmetros de URL fornecidos.
    - **profileIds**: O limite é 6 profiles.
    """
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Obtém as credenciais do hotel e lança erro 404 caso o hotel não exista
        hotel_credentials = Credentials(hotelId)

        search = get_profiles(hotel_credentials, profileId)

        if search['status'] == 200:
            return search['content']
        else:
            raise HTTPException(status_code=search['status'], detail=search['content'])
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException as e:
        raise e  # Se o erro for do tipo HTTPException, re-levante-o
    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro))