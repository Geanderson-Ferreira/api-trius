import requests
import json
from src.credentials import Credentials


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
                    cpf: str,
                    gender: str,
                   ):
    birth_date_str = date_of_birth.strftime('%Y-%m-%d')
    
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
    print('\n')
    print(profile_json)
    print('\n'
          )
    
    
    payload = json.dumps(profile_json)
    headers = {
    'Content-Type': 'application/json',
    'x-app-key': credenciais.app_key,
    'x-hotelid': credenciais.hotel_id,
    'Authorization': f'Bearer {credenciais.token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:

        print("Cadastro criado.")

        data = response.json()

        prof_id_returned = data['links'][0]['href'].split('/')[-1]
        post_cpf = put_cpf(credenciais, prof_id_returned, cpf)

        return prof_id_returned
    else:
        print(response.text)
        
