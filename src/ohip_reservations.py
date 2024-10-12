import requests
from src.credentials import Credentials
from datetime import datetime

class Reservas:
    def __init__(self, credenciais: Credentials):
        self.credentials = credenciais
        self.search_results = None

    def get_reservations_by_checkout_date(self, checkoutDate: str):

        try:
            datetime.strptime(checkoutDate, "%Y-%m-%d")
        except ValueError:
            return ValueError

        offset = 1
        hasMore = True
        reservas_list = []

        while hasMore:

            url = f"{self.credentials.api_url}/rsv/v1/hotels/{self.credentials.hotel_id}/reservations"

            params = {

                "departureStartDate": checkoutDate,
                "departureEndDate": checkoutDate,
                "limit": 200,
                "offset": offset,
                "excludePseudoRoomReservations": "true"
            }

            headers = {
            'Content-Type': 'application/json',
            'x-hotelid': self.credentials.hotel_id,
            'x-app-key': self.credentials.app_key,
            'Authorization': f'Bearer {self.credentials.token}'
            }

            response = requests.request("GET", url, headers=headers, params=params)

            if response.ok:
                response_data = response.json()
                offset = response_data['reservations']['offset']
                hasMore = response_data['reservations']['hasMore']

                reservas_list.extend(response_data['reservations']['reservationInfo'])

                if hasMore == False:
                    response_data['reservations']['reservationInfo'] = reservas_list
                    self.search_results = {
                        "responseStatus": 200,
                        "dataResult": response_data
                        }
            else:
                print(f"Erro ao obter reservas: {response.text}")
                hasMore = False
                self.search_results = {
                    "responseStatus": response.status_code,
                    "detail": response.text
                }

    def find_reservation_inside_of_results(self, lastName=None, reservationNumber=None, firstName=None):

        if self.search_results['responseStatus'] != 200:
            return {"responseStatus":self.search_results['responseStatus'],
                    "Error": self.search_results['detail']}

        resultado_final = []
        reservas_verificadas = []
        reservas = self.search_results["dataResult"]['reservations']['reservationInfo']

        for reserva in reservas:

            #Lê os atributos do json para o filtro
            first_name = reserva.get("reservationGuest", {}).get('givenName', '')
            surname = reserva.get("reservationGuest", {}).get('surname', '')
            opera_confirmation = reserva.get('reservationIdList', [{}, {}])[1].get('id', '')
            external_references = [ x['id'] for x in reserva.get('externalReferences', [])]
            resv_id = reserva.get('reservationIdList')[0].get('id')

            opera = bool( reservationNumber == opera_confirmation or reservationNumber is None)
            ext =bool(reservationNumber in external_references or reservationNumber is None)
            last = bool(str(lastName).lower() in list(map(lambda x: str(x).lower(), surname.split(' '))) or lastName is None)
            first = bool(str(firstName).lower() in list(map(lambda x: str(x).lower(), first_name.split(' '))) or firstName is None)

            if opera:
                print(f"""
                    conf: {opera_confirmation}
                    opera: {opera}
                    ext: {ext}
                    last: {last}
                    first: {first}
    ___________________________
                """)

            # Faz o filtro das condicoes
            filter_conditions = bool(
                bool(
                
                    bool(reservationNumber in external_references or reservationNumber is None or str(reservationNumber) == str(opera_confirmation))
                    and
                    bool( str(reservationNumber) == str(opera_confirmation) or reservationNumber is None)
                    and
                    bool(str(lastName).lower() in list(map(lambda x: str(x).lower(), surname.split(' '))) or lastName is None)
                    and
                    bool(str(firstName).lower() in list(map(lambda x: str(x).lower(), first_name.split(' '))) or firstName is None) 
            
                )
                and
                    resv_id not in reservas_verificadas
                
                and not
                
                    bool(lastName is None and reservationNumber is None and firstName is None)
            )


            #Para cada vez que o filtro pegar, inclui na lista de resultados
            if filter_conditions:

                share_ids = [x['profileId']['id'] for x in reserva.get('sharedGuests', [])]
                list_of_shared_reservations = [x for x in reservas if x['reservationIdList'][0]['id'] in share_ids]
                list_of_shared_reservations.append(reserva)
                
                total_adults = sum([
                    int(x.get('roomStay', {}).get('adultCount', 0)) 
                        for x in list_of_shared_reservations
                    ])
                
                total_childs = sum([
                    int(reserva.get('roomStay', {}).get('childCount', 0)) 
                        for reserva in list_of_shared_reservations
                    ])
                

                guests = [
                    {
                        "profileId": reserva['reservationGuest']['id'],
                        "firstName": reserva['reservationGuest']['givenName'],
                        "lastName": reserva['reservationGuest']['surname']
                    } for reserva in list_of_shared_reservations
                ]

                reservas_verificadas.extend(share_ids)
                
                resultado_final.append(
                    {

                        "adultNumber": total_adults,
                        "childnumber": total_childs,
                        "arrivalDate": reserva.get('roomStay', {}).get('arrivalDate', 0),
                        "departureDate": reserva.get('roomStay', {}).get('departureDate', 0),
                        "rateAmount": reserva.get('roomStay', {}).get('rateAmount', {}).get('amount', ''),
                        "guaranteeCode": reserva.get('roomStay', {}).get('guarantee', {}).get('guaranteeCode', ''),
                        "guests": guests
                    }
                )

        return {"responseStatus": 200,
                "dataResult": resultado_final}
