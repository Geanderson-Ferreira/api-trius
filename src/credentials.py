from src.token_manager import get_credentials, get_token

class Credentials:

    def __init__(self, hotel=None):

        self.credentials = get_credentials(hotel)

        self.api_url = self.credentials['hotel_url']
        self.app_key = self.credentials['hotel_appkey']
        self.client_id = self.credentials['hotel_clientid']
        self.hotel_id = self.credentials['hotel_code']
        self.token = self._get_token()

    def _get_token(self):

        token = get_token(self.hotel_id)
        return token
    
    def get_fake_cpf(self):
        return '99999999999'
    
