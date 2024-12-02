import psycopg, requests
from datetime import date, datetime, timedelta
from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException, status
from src.utils import api_return

load_dotenv()

def get_credentials(hotel):
    DATA_BASE_NAME = environ.get('DATA_BASE_NAME')
    DATA_BASE_USER = environ.get('DATA_BASE_USER')
    DATA_BASE_URL = environ.get('DATA_BASE_URL')
    DATA_BASE_PASSWORD = environ.get('DATA_BASE_PASSWORD')
    DATA_BASE_PORT = environ.get('DATA_BASE_PORT')
    ENVIRON = environ.get('ENVIRON')

    try:
        # Estabelecendo a conexão com o banco de dados
        conn = psycopg.connect(
            f"dbname={DATA_BASE_NAME} user={DATA_BASE_USER} password={DATA_BASE_PASSWORD} host={DATA_BASE_URL} port={DATA_BASE_PORT}"
        )

        cur = conn.cursor()

        # Consulta para verificar as credenciais do hotel
        selectCredentials = f"""SELECT * FROM "{ENVIRON}"."hotels" WHERE "hotel_code"='{hotel}';"""
        cur.execute(selectCredentials)
        hotelReturn = cur.fetchone()

    except psycopg.OperationalError as e:
        print(f"Erro ao conectar banco de dados: {e}")

        raise HTTPException(
                status_code=400,
                detail="Erro Interno. Contate o administrador da API.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Se não encontrar o hotel, lança um erro 404
    if hotelReturn is None:
        raise HTTPException(
                status_code=404,
                detail="Hotel não encontrado.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Se o hotel for encontrado, retorna as credenciais
    hotel_code = hotelReturn[1]
    hotel_name = hotelReturn[2]
    hotel_username = hotelReturn[3]
    hotel_password = hotelReturn[4]
    hotel_appkey = hotelReturn[5]
    hotel_clientid = hotelReturn[6]
    hotel_clientsecret = hotelReturn[7]
    hotel_url = hotelReturn[10]
    hotel_authkey = hotelReturn[11]

    credentials = {
        'hotel_code': hotel_code,
        'hotel_name': hotel_name,
        'hotel_username': hotel_username,
        'hotel_password': hotel_password,
        'hotel_appkey': hotel_appkey,
        'hotel_clientid': hotel_clientid,
        'hotel_clientsecret': hotel_clientsecret,
        'hotel_url': hotel_url,
        'hotel_authkey': hotel_authkey
    }

    return credentials


def update_token(hotel):

    DATA_BASE_NAME = environ.get('DATA_BASE_NAME')
    DATA_BASE_USER = environ.get('DATA_BASE_USER')
    DATA_BASE_URL = environ.get('DATA_BASE_URL')
    DATA_BASE_PASSWORD = environ.get('DATA_BASE_PASSWORD')
    DATA_BASE_PORT = environ.get('DATA_BASE_PORT')
    ENVIRON = environ.get('ENVIRON')

    #Tenta conectar ao banco
    try:
        conn = psycopg.connect(
            f"dbname={DATA_BASE_NAME} user={DATA_BASE_USER} password={DATA_BASE_PASSWORD} host={DATA_BASE_URL} port={DATA_BASE_PORT}"
        )
        selectCredentials = f"""

        Select * from "{ENVIRON}"."hotels" where "hotel_code"='{hotel}';
        
        """

        cur = conn.cursor()
        cur.execute(selectCredentials)
        hotelReturn = cur.fetchone()
    except psycopg.OperationalError as e:
        print(f"Erro ao conectar banco de dados: {e}")

        raise HTTPException(
                status_code=400,
                detail="Erro Interno. Contate administrador da API.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    hotel_code = hotelReturn[1]
    hotel_name = hotelReturn[2]
    hotel_username = hotelReturn[3]
    hotel_password = hotelReturn[4]
    hotel_appkey = hotelReturn[5]
    hotel_clientid = hotelReturn[6]
    hotel_clientsecret =hotelReturn[7]
    hotel_url = hotelReturn[10]
    hotel_authkey = hotelReturn[11]

    url = f"{hotel_url}/oauth/v1/tokens"

    payload = {'username':hotel_username,
               'password':hotel_password,
               'grant_type':'password'}
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-app-key': hotel_appkey,
    'Authorization': f'Basic {hotel_authkey}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"Token OHIP atualizado. Hotel: {hotel}")

    if response.ok:
        
        token = response.json()['access_token']

        updateToken = f"""update "{ENVIRON}"."hotels" set "hotel_token"='{token}', "hotel_tokentime"='{datetime.now()}' where "hotel_code"='{hotel}';"""
        cur.execute(updateToken)
        conn.commit()

        return token
    else:

        print(f"Erro ao obter Token do hotel {hotel_name}")

def get_token(hotel):

    DATA_BASE_NAME = environ.get('DATA_BASE_NAME')
    DATA_BASE_USER = environ.get('DATA_BASE_USER')
    DATA_BASE_URL = environ.get('DATA_BASE_URL')
    DATA_BASE_PASSWORD = environ.get('DATA_BASE_PASSWORD')
    DATA_BASE_PORT = environ.get('DATA_BASE_PORT')
    ENVIRON = environ.get('ENVIRON')

    try:
        conn = psycopg.connect(
            f"dbname={DATA_BASE_NAME} user={DATA_BASE_USER} password={DATA_BASE_PASSWORD} host={DATA_BASE_URL} port={DATA_BASE_PORT}"
        )
        cur = conn.cursor()

        selectCredentials = f"""Select * from "{ENVIRON}"."hotels" where "hotel_code"='{hotel}';"""
        cur.execute(selectCredentials)
        hotelReturn = cur.fetchone()

    except psycopg.OperationalError as e:
        print(f"Erro ao conectar banco de dados: {e}")

        raise HTTPException(
                status_code=400,
                detail="Erro Interno. Contate administrador da API.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    hotel_code = hotelReturn[1]
    hotel_name = hotelReturn[2]
    hotel_username = hotelReturn[3]
    hotel_password = hotelReturn[4]
    hotel_appkey = hotelReturn[5]
    hotel_clientid = hotelReturn[6]
    hotel_clientsecret = hotelReturn[7]
    hotel_token = hotelReturn[8]
    hotel_tokentime = hotelReturn[9]
    hotel_url = hotelReturn[10]
    hotel_authkey = hotelReturn[11]

    hotel_tokentime = datetime.strptime(hotel_tokentime, "%Y-%m-%d %H:%M:%S.%f")

    if datetime.now() - hotel_tokentime > timedelta(minutes=20):
        return update_token(hotel)
    else:
        return hotel_token