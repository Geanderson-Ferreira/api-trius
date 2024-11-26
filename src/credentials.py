class Credentials:

    def __init__(self, user=None, hotel=None):
        self.api_url = "https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com"
        self.app_key = '5502014f-a4f1-4135-9d45-ae5fd594eba5'
        self.client_id = 'ACCORAT_Client'
        self.hotel_id = 'H9087'
        self.token = self._get_token()

    def _get_token(self):
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTczMjY0MTg2OSwib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3MzI2NDU0NjksIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiODJkMmI1NzctZDA4ZS00ZGJhLThmNTItMDUyM2JkOWE1NDczIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.lIoDlOOCUIcG8Wrf57cCqe616lgu1tNb2rUPWeD8BR1gRsr1UZb1MZAWawFaL1N4F0ZysYt7aRCbjmlliURpefBvQAJCk1-0b3GTW-n0eNynmavw4jhYv3xMLT52FWG5zKwcxfmRzWFwU_YPb97PVinMCBn2V-FjP8FOuGdBi6is6FfD3iIldtFq3yHD3by_SvzqbYJRmhtrcEESVJ7ZY-JF5iEo4npjVgrKzf47Qtmaa_jaYL6IxOsbXSSVF4Du1XgbrAagphw7Fogrq0jM3nJNnxeWwHwHkDV5a7Y4Omd70ckYa7KIZ2XRzKpLWVHvlG2D2pk80l-O9yVhYGe2LA"
    
    def get_fake_cpf(hotel):
        return '99999999999'