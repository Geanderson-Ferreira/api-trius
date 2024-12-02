from pydantic import BaseModel
import jwt
import datetime
import psycopg
from os import environ
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
import datetime

load_dotenv()

# Definição do banco de dados a ser utilizado
DATA_BASE_NAME = environ.get('DATA_BASE_NAME')
DATA_BASE_USER = environ.get('DATA_BASE_USER')
DATA_BASE_URL = environ.get('DATA_BASE_URL')
DATA_BASE_PASSWORD = environ.get('DATA_BASE_PASSWORD')
DATA_BASE_PORT = environ.get('DATA_BASE_PORT')

# Print out the database details to confirm they're loaded correctly
print(f"Connecting to database {DATA_BASE_NAME} at {DATA_BASE_URL}:{DATA_BASE_PORT}")

# Establishing the connection to the database
conn = psycopg.connect(
    f"dbname={DATA_BASE_NAME} user={DATA_BASE_USER} password={DATA_BASE_PASSWORD} host={DATA_BASE_URL} port=5432"
)

cur = conn.cursor()

# Definições de configuração
SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inicializa o roteador de autenticação
router = APIRouter()

# Modelo de usuário
class User(BaseModel):
    username: str
    password: str

# Modelo de token
class Token(BaseModel):
    access_token: str
    token_type: str

# Dependência para obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Função para criar um token
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Rota para autenticação e geração de token
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #user = User(username=form_data.username, password=form_data.password)  
    username = form_data.username
    password = form_data.password
    selectUser = f"""Select * from "baipass_uat"."users" where "username"='{username}' and "password"='{password}';"""
    cur.execute(selectUser)
    userExists = cur.fetchone()

    if userExists == None:
        mensagemRetorno = 'Nome de usuário e/ou senha inválido!'
        return mensagemRetorno

    else:
        
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
