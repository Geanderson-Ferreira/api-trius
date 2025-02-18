import mysql
from dotenv import load_dotenv
from os import environ
import mysql.connector
import mysql
import requests
import base64

load_dotenv()


LEVEL_LOG="TERMINAL"
DATA_BASE_NAME=environ['DATA_BASE_NAME']
DATA_BASE_USER=environ['DATA_BASE_USER']
DATA_BASE_URL=environ['DATA_BASE_URL']
DATA_BASE_PASSWORD=environ['DATA_BASE_PASSWORD']
DATA_BASE_PORT=environ['DATA_BASE_PORT']


class Credentials:
    

    def __init__(self, hotel=None):

        query = """SELECT `INTEGRA_HOTEIS`.`HOTEL_ID`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_HOST`,
                        `INTEGRA_HOTEIS`.`HOTEL_APP_KEY`,
                        `INTEGRA_HOTEIS`.`HOTEL_CLIENT_ID`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_TOKEN`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_TOKEN_VALITY`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_USER`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_PASSWORD`,
                        `INTEGRA_HOTEIS`.`HOTEL_API_CLIENT_SECRET`,
                        `INTEGRA_HOTEIS`.`HOTEL_CLIENT_ID`
                  
                  FROM `integracaogean`.`INTEGRA_HOTEIS`
                  
                  WHERE HOTEL_ID = %s;"""

        conn = mysql.connector.connect(
                database=DATA_BASE_NAME,
                user=DATA_BASE_USER,
                host=DATA_BASE_URL,
                password=DATA_BASE_PASSWORD,
                port=DATA_BASE_PORT
            )
        
        cursor = conn.cursor()

        cursor.execute(query, (hotel,))

        dados = cursor.fetchone()

        self.api_url = dados[1]
        self.app_key = dados[2]
        self.client_id = dados[3]
        self.hotel_id = dados[0]
        self.token = dados[4]
        valit = dados[5]
        self.user = dados[6]
        self.password = dados[7]
        self.client_id = dados[8]
        self.client_secret = dados[9]

        
        self._get_token()
        print(self.token)


    def _get_token(self):

        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode()).decode()

        url = f"{self.api_url}/oauth/v1/tokens"

        payload = {
            'username': self.user,
            'password': self.password,
            'grant_type': 'password'
        } 

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-app-key': self.app_key,
        'Authorization': f'Basic {auth_base64}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.ok:
            self.token = response.json()['access_token']

        else:
            print("Erro ao obter token")