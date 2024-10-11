import requests
from credentials import Credentials
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
                    self.search_results = response_data
            else:
                print(f"Erro ao obter reservas: {response.text}")
                hasMore = False
                self.search_results = None

    def find_reservation_inside_of_results(self, lastName=None, reservationNumber=None, firstName=None):

        if self.search_results == None:
            return None

        resultado_final = []

        reservas = self.search_results['reservations']['reservationInfo']

        for reserva in reservas:
            first_name = reserva.get("reservationGuest", {}).get('givenName', '')
            surname = reserva.get("reservationGuest", {}).get('surname', '')
            opera_confirmation = reserva.get('reservationIdList', [{}, {}])[1].get('id', '')
            external_references = [ x['id'] for x in reserva.get('externalReferences', [])]

            filter_conditions = bool(
                reservationNumber in external_references # procura no external references
                or
                reservationNumber == opera_confirmation # procura no opera confirmation também
                or
                lastName in surname.split(' ') # Faz uma lista de sobrenomes para procurar
                or
                firstName in first_name.split(' ') # Procura pelo ultimo nome também
            )

            if filter_conditions:
                resultado_final.append(reserva)

        return resultado_final

r = Reservas(Credentials())
r.get_reservations_by_checkout_date('2024-10-10')
reserva_final = r.find_reservation_inside_of_results(lastName='SANTOS')

print(reserva_final)


