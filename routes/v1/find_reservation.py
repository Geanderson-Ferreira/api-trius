from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme
from src.ohip_reservations import find_reservation_inside_of_results, get_reservations_by_checkout_date
from src.credentials import Credentials

ROTA = "/find-reservation"

router = APIRouter()

class DateResponse(BaseModel):
    date: str

@router.get(ROTA)
async def find_reservation(
    hotel: str,
    checkoutDate: str = None,
    checkinDate: str = None,
    reservationNumber: str = None,
    firstname: str = None,
    lastName: str = None,
    token: str = Depends(oauth2_scheme)
):

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if checkinDate is None and checkoutDate is None:
        raise HTTPException(status_code=400, detail="Criterios Minimos nao informados, informe pelo menos uma data de hospedagem.")

    try:
        if checkoutDate is not None:
            datetime.strptime(checkoutDate, "%Y-%m-%d")
        if checkinDate is not None:
            datetime.strptime(checkinDate or '', "%Y-%m-%d")
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    if checkinDate is None and checkoutDate is None:
        raise HTTPException(status_code=400, detail="Criterios Minimos nao informados, informe pelo menos uma data de hospedagem.")

    reservas_do_dia = get_reservations_by_checkout_date(Credentials(hotel), checkoutDate, checkinDate)

    if reservas_do_dia.get('responseStatus') != 200:
        raise HTTPException(status_code=404, detail="Reservations for the specified checkout date not found.")

    resultado = find_reservation_inside_of_results(
        hotelId=hotel,
        search_results=reservas_do_dia,
        lastName=lastName,
        reservationNumber=reservationNumber,
        firstName=firstname
    )

    if resultado.get('responseStatus') != 200:
        raise HTTPException(status_code=404, detail=resultado.get('Error', 'No results found.'))


    return resultado.get('dataResult', [])
