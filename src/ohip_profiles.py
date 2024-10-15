import requests
import json
from src.credentials import Credentials
from fastapi import HTTPException

def get_profiles(credenciais: Credentials, profile_id_list):

    credenciais = Credentials(credenciais.hotel_id)
    any_success = False

    resultado = []
    for profile in profile_id_list:
    
        url = f"{credenciais.api_url}/crm/v1/profiles/{profile}"

        # Defina os parâmetros diretamente
        params = {
            'fetchInstructions': [
                'Address', 'Comment', 'Communication', 'Correspondence',
                'DeliveryMethods', 'FutureReservation', 'GdsNegotiatedRate',
                'HistoryReservation', 'Indicators', 'Keyword', 'Membership',
                'NegotiatedRate', 'Preference', 'Profile', 'Relationship',
                'SalesInfo', 'Subscriptions', 'WebUserAccount'
            ]
        }

        payload = {}
        headers = {
            'x-app-key': credenciais.app_key,
            'x-hotelid': credenciais.hotel_id,
            'Authorization': f'Bearer {credenciais.token}'
        }

        # Faça a requisição com os parâmetros
        
        response = requests.get(url, headers=headers, params=params)

        if response.ok:

            profile_json = response.json()
            
            full_name = profile_json.get('profileDetails',{}).get('customer',{}).get('personName',[{}])[0].get('givenName')
            nacionalidade = profile_json.get('profileDetails',{}).get('customer',{}).get('citizenCountry',{}).get('code')
            date_of_birth = profile_json.get('profileDetails',{}).get('customer',{}).get('birthDate')
            email = profile_json.get('profileDetails',{}).get('emails',{}).get('emailInfo',[{}])[0].get('email',{}).get('emailAddress')
            telephone = profile_json.get('profileDetails',{}).get('telephones',{}).get('telephoneInfo',[{}])[0].get('telephone',{}).get('phoneNumber')
            country = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('country',{}).get('code')
            zip_code = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('postalCode')
            

            address_line = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('addressLine')

            street = address_line[0] if len(address_line) > 0 else None
            numero_residencial =  address_line[1] if len(address_line) > 1 else None
            if str(numero_residencial).isdigit():
                numero_residencial = int(numero_residencial)
            else: numero_residencial = None

            bairro = address_line[2] if len(address_line) > 2 else None
            complemento = address_line[3] if len(address_line) > 3 else None
            cidade = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('cityName')
            estado = profile_json.get('profileDetails',{}).get('addresses',{}).get('addressInfo',[{}])[0].get('address',{}).get('state')
            cpf = profile_json.get('profileDetails',{}).get('taxInfo',{}).get('tax1No')
            gender = profile_json.get('profileDetails',{}).get('customer',{}).get('gender')


            dados = {
                'fullName': full_name,
                'citizenCountry': nacionalidade,
                'dateOfBirth': date_of_birth,
                'email': email,
                'telephone': telephone,
                'residenceCountry': country,
                'zipCode': zip_code,
                'street': street,
                'residenceNumber': numero_residencial,
                'neighborhood': bairro,
                'complement': complemento,
                'city': cidade,
                'state': estado,
                'cpf': cpf,
                'gender': gender
            }

            resultado.append({profile: dados})
            any_success = True
        else:
            resultado.append({profile: response.text})

    if any_success:
        return {"status": 200, "content": resultado}
    else:
        return {"status": response.status_code, "content": response.text}

def put_cpf(credencials: Credentials, profile_id, cpf):


    url = f"{credencials.api_url}/crm/v1/profiles/{profile_id}"

    payload = json.dumps({
    "profileDetails": {
        "taxInfo": {
        "tax1No": cpf
        }
    },
    "profileIdList": [
        {
        "type": "Profile",
        "id": profile_id
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'x-app-key': credencials.app_key,
    'x-hotelid': credencials.hotel_id,
    'Authorization': f'Bearer {credencials.token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    if response.ok:
        print("CPF Inserido.")


def create_profile(credenciais: Credentials,        
                    full_name: str,
                    citizen_country: str,
                    date_of_birth: str,
                    email: str,
                    telephone: str,
                    residence_country: str,
                    zip_code: str,
                    street: str,
                    residence_number: str,
                    neighborhood: str,
                    complement: str,
                    city: str,
                    state: str,
                    cpfOrPassport: str,
                    gender: str,
                   ):
    birth_date_str = date_of_birth.strftime('%Y-%m-%d')

    is_estrangeiro = bool(citizen_country != 'BR')

    if is_estrangeiro:
        doc = 'PASSPORT'
        cpf_fake = credenciais.get_fake_cpf()
    else:
        doc = 'CPF'
        

    
    name = full_name.split(' ')

    if len(name) > 1:
        first_name = ' '.join(name[:-1])
        last_name = name[-1]
        
    if len(name) == 1:
        first_name = name[0]
        last_name = name[0]


    url = f"{credenciais.api_url}/crm/v1/profiles"

    profile_json = {
    "profileDetails": {
        "customer": {
            "identifications": {
                    "identificationInfo": [
                    {
                        "identification": {
                        "idType": doc,
                        "idNumber": cpfOrPassport,
                        "primaryInd": True
                        }
                    }
                    ]
                },
        "personName": [
            {
            "givenName": first_name,
            "surname": last_name,
            "nameType": "Primary"
            },
            {
            "nameType": "Alternate"
            },
            {
            "nameType": "Incognito"
            }
        ],

        
        "alienInfo": {},
        "birthCountry": {
            "code": citizen_country
        },
        
        "gender": gender,
        "birthDate": birth_date_str,
        "language": "E"
        },
        "addresses": {
        "addressInfo": [
            {
            "address": {
                "isValidated": False,
                "addressLine": [
                street,
                residence_number,
                neighborhood,
                complement
                ],
                "cityName": city,
                "postalCode": zip_code,
                "state": state,
                "country": {
                "value": residence_country
                },
                "language": "E",
                "type": "BUSINESS",
                "primaryInd": True
            }
            }
        ]
        },
        "telephones": {
        "telephoneInfo": [
            {
            "telephone": {
                "phoneTechType": "PHONE",
                "phoneUseType": "HOME",
                "phoneNumber": telephone,
                "orderSequence": "1",
                "primaryInd": True
            }
            }
        ]
        },

        "emails": {
        "emailInfo": [
            {
            "email": {
                "emailAddress": email,
                "type": "EMAIL",
                "typeDescription": "Email Address",
                "primaryInd": True
            }
            }
        ]
        },
        "mailingActions": {
        "active": True
        },
        "privacyInfo": {
        "marketResearchParticipation": True,
        "infoFromThirdParty": True,
        "autoEnrollLoyaltyProgram": False,
        "allowPhone": True,
        "allowSMS": True,
        "allowEmail": True,
        "optInMailingList": True,
        "optInMarketResearch": True,
        "optInThirdParty": True,
        "optInAutoEnrollmentMember": True,
        "optInPhone": True,
        "optInSms": True,
        "optInEmail": True
        },
        "statusCode": "Active",
        "requestForHotel": credenciais.hotel_id,
        "markAsRecentlyAccessed": True,
        "profileType": "Guest"
    },
    "profileIdList": []
    }

    payload = json.dumps(profile_json)
    headers = {
    'Content-Type': 'application/json',
    'x-app-key': credenciais.app_key,
    'x-hotelid': credenciais.hotel_id,
    'Authorization': f'Bearer {credenciais.token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:

        data = response.json()

        prof_id_returned = data['links'][0]['href'].split('/')[-1]

        if is_estrangeiro:
            post_cpf = put_cpf(credenciais, prof_id_returned, cpf_fake)
        else:
            post_cpf = put_cpf(credenciais, prof_id_returned, cpfOrPassport)
        
        dados = get_profiles(credenciais, [prof_id_returned])

        if dados['status'] != 200:
            dados = {'status': 200, 'content': f'Cadastro criado com sucesso, mas erro no get: {dados['content']}'}

    else:
        dados = {'status': 400, 'content': response.text}

    return dados