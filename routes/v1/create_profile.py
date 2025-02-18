from fastapi import APIRouter, Depends, HTTPException
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY
from src.ohip_profiles import create_or_update_profile
from src.credentials import Credentials
from models.models import GuestProfile

ROTA = "/create-profile"


# Inicializa o roteador de clientes
router = APIRouter()


# Novo endpoint para receber o perfil do cliente
@router.post(ROTA)
async def create_customer_profile(hotel, profile: GuestProfile, token: str = Depends(oauth2_scheme)):

    """
    Rota cria o cadastro de um hóspede.
    o valor *citzenCountry* refere-se à nacionalidade do hóspede.

    Se ele não for brasileiro, não é necessário passar um endereço completo. Basta passar um *residenceCountry*
    e os demais valores de endereço como strings vazias.
    
    *gender* aceita: 'Male', 'Female' e 'Unknown'

    """
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
 
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    print(hotel)

    credenciais = Credentials(hotel)

    print(credenciais.token)

    profile_criado = create_or_update_profile(credenciais, profile.fullName, profile.citizenCountry, profile.dateOfBirth,
                    profile.email, profile.telephone, profile.residenceCountry,
                    profile.zipCode, profile.street, profile.residenceNumber,
                    profile.neighborhood, profile.complement, profile.city, profile.state,
                    profile.cpfOrPassport, profile.gender)

    if profile_criado['status'] == 200:
        return profile_criado['content']
    else:
        raise HTTPException(status_code=401, detail=profile_criado['content'])
    