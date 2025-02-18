from pydantic import BaseModel
import jwt
import datetime
from os import environ
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
# import jwt
from jose import jwt  # Caso esteja usando python-jose ao invés de PyJWT
import datetime
from src.utils import api_return
import mysql
from dotenv import load_dotenv
from os import environ
import mysql.connector
import mysql


load_dotenv()

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

    #Pega os dados enviados pelo usuário
    username = form_data.username
    password = form_data.password
    
    LEVEL_LOG="TERMINAL"
    DATA_BASE_NAME=environ['DATA_BASE_NAME']
    DATA_BASE_USER=environ['DATA_BASE_USER']
    DATA_BASE_URL=environ['DATA_BASE_URL']
    DATA_BASE_PASSWORD=environ['DATA_BASE_PASSWORD']
    DATA_BASE_PORT=environ['DATA_BASE_PORT']

    conn = mysql.connector.connect(
                database=DATA_BASE_NAME,
                user=DATA_BASE_USER,
                host=DATA_BASE_URL,
                password=DATA_BASE_PASSWORD,
                port=DATA_BASE_PORT
            )
        
    cur = conn.cursor()

    selectUser = f"""
        SELECT `INTEGRA_API_USERS`.`API_USERNAME`,
            `INTEGRA_API_USERS`.`API_PASSWORD`,
            `INTEGRA_API_USERS`.`API_USER_TYPE`
        FROM `integracaogean`.`INTEGRA_API_USERS`
        WHERE `INTEGRA_API_USERS`.`API_USERNAME` = %s
        AND `INTEGRA_API_USERS`.`API_PASSWORD` = %s;
        """



    cur.execute(selectUser, (username, password))
    userExists = cur.fetchone()

    if userExists is None:
        api_return(401, 'Usuário não autorizado.')

    else:
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
