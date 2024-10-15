class Credentials:

    def __init__(self, user=None, hotel=None):
        self.api_url = "https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com"
        self.app_key = '5502014f-a4f1-4135-9d45-ae5fd594eba5'
        self.client_id = 'ACCORAT_Client'
        self.hotel_id = 'H5519'
        self.token = self._get_token()

    def _get_token(self):
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcyODk0OTUxMywib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3Mjg5NTMxMTMsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiYjhlNDRlMGQtNzFmNC00MjMzLTllOGYtYjE5Mjc0MWY0ZWNhIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.Ka2AaagpFcoH5g8RP-3nDXumIl1eavpAeR-hOzMU8vhPYiZzUlFS4PPnr3wa38uVcDLoh1jgJKBBGGURU0CeA4ORxXk9muXJXOvs2RftA2D_JNgI6kU23WFHPsw8hY3s659oV7uRPHP580ZxBkmn7AFFMLMeBzhRKPvZHXTu7cR79VgFvRlrUKvd68BNIYukikNzT1jShCGPNSWvsrGVdCBHxb-jCF8bhs-a9W0lx0Vxwzj6z_tBupXQjKvetO8QxnwE9CgdBXHUzqOcu7g-lmmCxxrpCi4yK4sUo86kWg51uDX9bfYYid2Gm0ClHM4A6SIXPZchVnko6khK0g__eA"
    
    def get_fake_cpf(hotel):
        return '99999999999'