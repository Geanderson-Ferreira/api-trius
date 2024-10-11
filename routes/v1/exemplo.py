from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme
# Inicializa o roteador de exemplo
router = APIRouter()

# Modelo de resposta
class DateResponse(BaseModel):
    date: str

# Rota GET para receber um parâmetro de data
@router.get("/get-date", response_model=DateResponse)
async def get_date(data: str, token: str = Depends(oauth2_scheme)):
    # Verifica se o token é válido (a lógica de validação pode ser mais complexa em produção)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Valida a data recebida
    try:
        parsed_date = datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    return {"date": parsed_date.strftime("%Y-%m-%d")}
