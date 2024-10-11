from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme

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


@router.get(ROTA, response_model=DateResponse)
async def find_reservation(checkoutDate: str, reservationNumber: str, lastName: str, token: str = Depends(oauth2_scheme)):

    #Mais um check de Token
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    #Verifica o formato da data de checkout
    try:
        parsed_date = datetime.strptime(checkoutDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return {"date": parsed_date.strftime("%Y-%m-%d")}
