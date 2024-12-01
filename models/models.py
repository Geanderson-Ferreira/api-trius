
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, constr


class GuestProfile(BaseModel):
    fullName: str
    citizenCountry: constr(min_length=2, max_length=2)  # type: ignore
    dateOfBirth: date
    email: EmailStr
    telephone: str
    residenceCountry: constr(min_length=2, max_length=2)  # type: ignore 
    zipCode: str
    street: str
    residenceNumber: Optional[str]
    neighborhood: str
    complement: Optional[str]
    city: str
    state: constr(max_length=2)  # type: ignore # código do estado com 2 caracteres
    cpfOrPassport: constr(max_length=11)  # type: ignore # CPF com 11 caracteres
    gender: Optional[str]

class ShareRequestBody(BaseModel):
    reservationIdParent: int
    shareProfileId: int