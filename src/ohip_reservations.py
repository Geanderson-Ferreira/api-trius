import requests
from src.credentials import Credentials
from datetime import datetime
import json 

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
            external_references = [ str(x['id']) for x in reserva.get('externalReferences', [])]
            resv_id = reserva.get('reservationIdList')[0].get('id')

            opera = bool( reservationNumber == opera_confirmation or reservationNumber is None)
            ext =bool(reservationNumber in external_references or reservationNumber is None)
            last = bool(str(lastName).lower() in list(map(lambda x: str(x).lower(), surname.split(' '))) or lastName is None)
            first = bool(str(firstName).lower() in list(map(lambda x: str(x).lower(), first_name.split(' '))) or firstName is None)

            # Faz o filtro das condicoes
            filter_conditions = bool(
                bool(
                    bool(str(reservationNumber) in external_references or reservationNumber is None or str(reservationNumber) == str(opera_confirmation))
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


def get_reservation(credentials, resv_id):

    url = f"{credentials.api_url}/rsv/v1/hotels/{credentials.hotel_id}/reservations/{resv_id}?fetchInstructions=Reservation&fetchInstructions=Comments&fetchInstructions=GuestMemberships&fetchInstructions=GuestLastStay&fetchInstructions=ProfileAwards&fetchInstructions=ScheduledActivities&fetchInstructions=ReservationAwards&fetchInstructions=Tickets&fetchInstructions=GuestComments&fetchInstructions=Packages&fetchInstructions=InventoryItems&fetchInstructions=ReservationPaymentMethods&fetchInstructions=RoutingInstructions&fetchInstructions=Preferences&fetchInstructions=Memberships&fetchInstructions=Alerts&fetchInstructions=Traces&fetchInstructions=ConfirmationLetters&fetchInstructions=CallHistory&fetchInstructions=FixedCharges&fetchInstructions=GuestMessages&fetchInstructions=ReservationPolicies&fetchInstructions=Indicators&fetchInstructions=LinkedReservations&fetchInstructions=ECoupons&fetchInstructions=TrackItItems&fetchInstructions=WebRegistrationCards&fetchInstructions=ReservationActivities&fetchInstructions=PrepaidCards&fetchInstructions=Attachments&fetchInstructions=Locators&fetchInstructions=TransactionDiversions&fetchInstructions=ECertificates&fetchInstructions=UpsellInfo&fetchInstructions=RoomAssignedByAI&fetchInstructions=RevenuesAndBalances"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': credentials.hotel_id,
    'x-app-key': credentials.app_key,
    'Authorization': f'Bearer {credentials.token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:

        return response.json()
    else:
        print(f"Reserva {resv_id} não obtida")
        return False

def new_reservation(credentials, checkin_date, checkout_date, room_type,
                    rate_plan_code, market_code, market_code_description,
                    source_code, source_code_description, first_name, last_name,
                    payment_method, guarantee_code, guarantee_code_description,
                    comment, comment2, external_reference, external_reference_type):


    hotel = credentials.hotel_id
    tarifa = '0'            #ok
    moeda = 'BRL'           #ok
    adult_number = '1'      #ok
    child_number = '0'      #ok
    number_of_rooms = '1'   #ok

    url = f"{credentials.api_url}/rsv/v1/hotels/{credentials.hotel_id}/reservations"

    payload = json.dumps({
    "reservations": {
        "reservation": [
        {
            "externalReferences": [
                    {
                        "id": external_reference,
                        "idExtension": 1,
                        "idContext": external_reference_type
                    }
                ]
            ,"sourceOfSale": {
            "sourceType": "PMS",
            "sourceCode": hotel
            },
            "roomStay": {
            "roomRates": [
                {
                "total": {
                    "amountBeforeTax": tarifa
                },
                "rates": {
                    "rate": [
                    {
                        "base": {
                        "amountBeforeTax": tarifa,
                        "currencyCode": moeda
                        },
                        "shareDistributionInstruction": "Full",
                        "total": {
                        "amountBeforeTax": tarifa
                        },
                        "start": checkin_date,
                        "end": checkout_date
                    }
                    ]
                },
                "guestCounts": {
                    "adults": adult_number,
                    "children": child_number
                },
                "roomType": room_type,
                "ratePlanCode": rate_plan_code,
                "start": checkin_date,
                "end": checkout_date,
                "suppressRate": True,
                "marketCode": market_code,
                "marketCodeDescription": market_code_description,
                "sourceCode": source_code,
                "sourceCodeDescription": source_code_description,
                "numberOfUnits": number_of_rooms,
                "pseudoRoom": False,
                "roomTypeCharged": room_type,
                "houseUseOnly": False,
                "complimentary": False,
                "fixedRate": True,
                "discountAllowed": False,
                "bogoDiscount": False
                }
            ],
            "guestCounts": {
                "adults": adult_number,
                "children": child_number
            },
            "arrivalDate": checkin_date,
            "departureDate": checkout_date,
            "guarantee": {
                "guaranteeCode": guarantee_code,
                "shortDescription": guarantee_code_description
            },
            "roomNumberLocked": False,
            "printRate": False
            },
            "reservationGuests": [
            {
                "profileInfo": {
                "profile": {
                    "customer": {
                    "personName": [
                        {
                        "givenName": first_name,
                        "surname": last_name,
                        "nameType": "Primary"
                        },
                        {
                        "nameType": "External"
                        }
                    ],
                    "language": "E"
                    },
                    "profileType": "Guest"
                }
                },
                "primary": True
            }
            ],
            "reservationPaymentMethods": [
            {
                "paymentMethod": payment_method,
                "folioView": "1"
            }
            ],
            "comments": [
            {
                "comment": {
                "text": {
                    "value": comment
                },
                "commentTitle": "General Notes",
                "notificationLocation": "RESERVATION",
                "type": "GEN",
                "internal": False
                }
            },
            {
                "comment": {
                "text": {
                    "value": comment2
                },
                "commentTitle": "General Notes",
                "notificationLocation": "RESERVATION",
                "type": "GEN",
                "internal": False
                }
            }
            ],
            "hotelId": hotel,
            "overrideInventoryCheck": True,
            "roomStayReservation": True,
            "reservationStatus": "Reserved",
            "walkIn": False,
            "printRate": False,
            "preRegistered": False,
            "upgradeEligible": False,
            "allowAutoCheckin": False,
            "hasOpenFolio": False,
            "allowMobileCheckout": False,
            "allowMobileViewFolio": False,
            "allowPreRegistration": False,
            "optedForCommunication": False
        }
        ]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': credentials.app_key,
    'Authorization': f'Bearer {credentials.token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # OBTEM A RESERVA
    if response.status_code == 201:
        
        print("Reserva Criada com Sucesso.")

        get_reservation_url = [x for x in response.json()['links'] if x['operationId'] == 'getReservation'][0]['href']

        # print('\n', get_reservation_url)
        headers = {
        'Content-Type': 'application/json',
        'x-hotelid': hotel,
        'x-app-key': credentials['app_key'],
        'Authorization': f'Bearer {credentials.token}'
        }

        response = requests.request("GET", get_reservation_url, headers=headers, data=payload)
        
        if response.ok:
            reservation_id = response.json()['reservations']['reservation'][0]['reservationIdList'][0]['id']

            print(f"Reserva Obtida: {response.json()['reservations']['reservation'][0]['reservationIdList']}")
            
        else:
            print(f"Erro ao obter retorno da Reserva inserida: {response.text}")
        
        return {"inserida": True, "content": response.json()}
    else:
        print(f"Erro ao inserir reserva: {response.text}")
        return {"inserida": False}


def new_reservation_with_existing_profile(credentials, profile_id, checkin, checkout, payment_method, guarantee_code, source_code, amount, market_code, rate_plan_code, room_type):

    url = f"{credentials.api_url}/rsv/v1/hotels/{credentials.hotel_id}/reservations"

    payload = json.dumps({
    "reservations": {
        "reservation": {
        "reservationGuests": {
            "profileInfo": {
            "profileIdList": {
                "id": profile_id,
                "type": "Profile"
            }
            }
        },
        "reservationPaymentMethods": {
            "paymentMethod": payment_method
        },
        "markAsRecentlyAccessed": True,
        "hotelId": credentials.hotel_id,
        "reservationStatus": "Reserved",
        "roomStay": {
            "guarantee": {
            "onHold": False,
            "guaranteeCode": guarantee_code
            },
            "roomRates": {
            "sourceCode": source_code,
            "numberOfUnits": 1,
            "rates": {
                "rate": {
                "start": checkin,
                "end": checkout,
                "base": {
                    "amountBeforeTax": amount,
                    "currencyCode": "BRL"
                }
                }
            },
            "start": checkin,
            "marketCode": market_code,
            "end": checkout,
            "roomTypeCharged": "",
            "ratePlanCode": rate_plan_code,
            "roomType": room_type,
            "pseudoRoom": False
            },
            "guestCounts": {
            "children": 0,
            "adults": 1
            },
            "departureDate": checkout,
            "arrivalDate": checkin
        }
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': credentials.hotel_id,
    'x-app-key': credentials.app_key,
    'Authorization': f'Bearer {credentials.token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        print("Reserva criada")
        return {"action_status": 201, "content":response.json()}
    else:
        return {"action_status": 400, "content":response.text}


def create_share(credentials, resv_id_parent, share_profile_id):

    # Encontra a reserva original Parent para fazer as associações
    resv_parent_data = get_reservation(credentials, resv_id_parent)

    if not resv_parent_data:
        return {'status': 204, 'content': 'Não foi possível encontrar a reserva parent'}

    # Cria nova Reserva com as informações basicas da reserva parent
    checkin_date = resv_parent_data['reservations']['reservation'][0]['roomStay']['arrivalDate']
    checkout_date = resv_parent_data['reservations']['reservation'][0]['roomStay']['departureDate']
    room_type = resv_parent_data['reservations']['reservation'][0]['roomStay']['roomRates'][0]['roomType']
    rate_plan_code = resv_parent_data['reservations']['reservation'][0]['roomStay']['roomRates'][0]['ratePlanCode']
    market_code = resv_parent_data['reservations']['reservation'][0]['roomStay']['roomRates'][0]['marketCode']
    source_code = resv_parent_data['reservations']['reservation'][0]['roomStay']['roomRates'][0]['sourceCode']
    payment_method = resv_parent_data['reservations']['reservation'][0]['reservationPaymentMethods'][0]['paymentMethod']
    guarantee_code = resv_parent_data['reservations']['reservation'][0]['roomStay']['guarantee']['guaranteeCode']

    nova_reserva = new_reservation_with_existing_profile(credentials, share_profile_id, checkin_date, checkout_date, payment_method, guarantee_code, source_code, '0', market_code, rate_plan_code, room_type)

    if nova_reserva['action_status'] != 201:
        return {'status': 400, 'content': nova_reserva['content']}


    # Atribui Share
    share_reservation_id = [x['href'] for x in nova_reserva['links'] if x['operationId'] == 'getReservation'][0].split('/')[:-1]


    return {'status': 200, 'content': resv_parent_data}


    # Faz o share
    