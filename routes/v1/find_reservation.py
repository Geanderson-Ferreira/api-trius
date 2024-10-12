from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme
from src.ohip_reservations import Reservas
from src.credentials import Credentials

ROTA = "/find-reservation"

"""
Endpoint deve retornar reservas referentes ao filtro checkoutDate, reservationNumber e lastName
-> checkoutDate é um parametro obrigatório.
-> buscar o json de todas as reservas com checkout nesse dia.
-> Usar esse Json para procurar os demais parametros solicitados.
-> Se houver reservationNumber, começa a procurar por ele.
-> Se não, começa a procurar pelo sobrenome / utilizar o tipo de busca LIKE e não exato.
"""

router = APIRouter()

class DateResponse(BaseModel):
    date: str

@router.get(ROTA)
async def find_reservation(hotel: str, checkoutDate: str, reservationNumber: str=None, firstname: str=None, lastName: str=None, token: str = Depends(oauth2_scheme)):

    #Mais um check de Token
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    #Verifica o formato da data de checkout
    try:
        datetime.strptime(checkoutDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    #Instacia de reservas com as credenciais do hotel carregadas
    ConsultaReservas = Reservas(
        Credentials(hotel)
        )

    ConsultaReservas.get_reservations_by_checkout_date(checkoutDate)

    resultado = ConsultaReservas.find_reservation_inside_of_results(
        lastName=lastName,
        reservationNumber=reservationNumber,
        firstName=firstname
    )

    if resultado['responseStatus'] != 200:
        raise HTTPException(status_code=401, detail=resultado['Error'])


    return resultado['dataResult']
