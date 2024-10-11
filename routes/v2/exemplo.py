from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from routes.v1.auth import oauth2_scheme
# Inicializa o roteador de exemplo
router = APIRouter()


@router.get("/init")
async def init():    
    return {"info": "versao em desenvolvimento."}
