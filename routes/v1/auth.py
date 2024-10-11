from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
import datetime

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
    user = User(username=form_data.username, password=form_data.password)  # Aqui você deve verificar o usuário no banco de dados
    if user.username != "admin" or user.password != "password":  # Exemplo de verificação
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
