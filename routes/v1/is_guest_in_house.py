from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme
from src.ohip_reservations import find_reservation_inside_of_results, get_reservations_by_checkout_date
from src.credentials import Credentials
from src.ohip_reservations import get_in_house_reservations, find_reservation_in_house
ROTA = "/is-guest-in-house"

router = APIRouter()

class DateResponse(BaseModel):
    date: str

@router.get(ROTA)
async def is_guest_in_house(
    hotel: str,
    roomNumber: str,
    fullName: str,
    token: str = Depends(oauth2_scheme)
):

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    
    in_house = get_in_house_reservations(credentials=Credentials(str(hotel)))
    resultado = find_reservation_in_house(search_results=in_house, fullName=fullName, roomNumber=roomNumber)

    return resultado
