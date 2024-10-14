from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from pydantic import BaseModel
from src.ohip_reservations import Reservas
from src.credentials import Credentials
from typing import List
import requests
import jwt
from routes.v1.auth import oauth2_scheme, SECRET_KEY

ROTA = "/get-profiles"

""""
Precisa retornar

Nacionalidade
Data de Nascimento
Email
Telefone
Endereço Pais
CEP
Rua
Numero
Bairro
Cidade
Estado

"""

router = APIRouter()

@router.get(ROTA)
async def get_profiles(hotelId:str, profileId: List[int] = Query(..., max_length=6), token: str = Depends(oauth2_scheme)):
    """Obtém perfis de hóspedes com base nos parâmetros de URL fornecidos.

    - **profileIds**:

    O limite é 6 profiles.

    """
    try:
        # Decodifica o token para verificar a autenticidade
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    credenciais = Credentials(hotelId)

    resultado = []
    for profile in profileId:
    
        url = f"{credenciais.api_url}/crm/v1/profiles/{profile}"

        # Defina os parâmetros diretamente
        params = {
            'fetchInstructions': [
                'Address', 'Comment', 'Communication', 'Correspondence',
                'DeliveryMethods', 'FutureReservation', 'GdsNegotiatedRate',
                'HistoryReservation', 'Indicators', 'Keyword', 'Membership',
                'NegotiatedRate', 'Preference', 'Profile', 'Relationship',
                'SalesInfo', 'Subscriptions', 'WebUserAccount'
            ]
        }

        payload = {}
        headers = {
            'x-app-key': credenciais.app_key,
            'x-hotelid': credenciais.hotel_id,
            'Authorization': f'Bearer {credenciais.token}'
        }

        # Faça a requisição com os parâmetros
        
        response = requests.get(url, headers=headers, params=params)

        if response.ok:

            profile_json = response.json()
            
            full_name = profile_json.get('profileDetails',{}).get('customer',{}).get('personName',[{}])[0].get('givenName')
            nacionalidade = profile_json.get('profileDetails',{}).get('customer',{}).get('citizenCountry',{}).get('code')
            date_of_birth = profile_json.get('profileDetails',{}).get('customer',{}).get('birthDate')
            email = profile_json.get('profileDetails',{}).get('emails',{}).get('emailInfo',[{}])[0].get('email',{}).get('emailAddress')
            telephone = profile_json.get('profileDetails',{}).get('telephones',{}).get('telephoneInfo',[{}])[0].get('telephone',{}).get('phoneNumber')
            country = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('country',{}).get('code')
            zip_code = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('postalCode')
            

            address_line = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('addressLine')

            street = address_line[0] if len(address_line) > 0 else None
            numero_residencial =  address_line[1] if len(address_line) > 1 else None
            if str(numero_residencial).isdigit():
                numero_residencial = int(numero_residencial)
            else: numero_residencial = None

            bairro = address_line[2] if len(address_line) > 2 else None
            complemento = address_line[3] if len(address_line) > 3 else None
            cidade = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('cityName')
            estado = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('state')
            cpf = profile_json.get('profileDetails',{}).get('taxInfo',{}).get('tax1No')
            gender = profile_json.get('profileDetails',{}).get('customer',{}).get('gender')


            dados = {
                'fullName': full_name,
                'citizenCountry': nacionalidade,
                'dateOfBirth': date_of_birth,
                'email': email,
                'telephone': telephone,
                'residenceCountry': country,
                'zipCode': zip_code,
                'street': street,
                'residenceNumber': numero_residencial,
                'neighborhood': bairro,
                'complement': complemento,
                'city': cidade,
                'state': estado,
                'cpf': cpf,
                'gender': gender
            }

            resultado.append({profile: dados})
        else:
            resultado.append({profile: response.text})

    return resultado
