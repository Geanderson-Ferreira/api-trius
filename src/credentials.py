class Credentials:

    def __init__(self, user=None, hotel=None):
        self.api_url = "https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com"
        self.app_key = '5502014f-a4f1-4135-9d45-ae5fd594eba5'
        self.client_id = 'ACCORAT_Client'
        self.hotel_id = 'H5519'
        self.token = self._get_token()

    def _get_token(self):
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcyODcwMDMzOCwib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3Mjg3MDM5MzgsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiZTgzZjMyNjItMjBhZi00ZDljLWFjZWQtZTM4ZTE1YWEwNGEzIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.emyyOrtd9aT_VQjcsthletFTIpF46oOt34V9tI-_JzFUdoHTR-OcKO086aPgdouBzaUJmWm452eu2bNZiWefFGC41lTU3dJndoQqtR2pAn-h0SVv_7vVuJwdMVaOSTtgWb9Vmp-k50Pd4cKzZbg8ZoI5PnRVovrEi5D7sJbEgYI5Kzfv3bhKklS-WW7_g11RPX8EVHftejPkc4sobeIQ_Bi098whGXEXW0RpS0OrW0ONb7-6Nt8A1gy8OxDNc_qGC4TjaceS019mDrme8XeKE0I6WzwClKluXXuLonNgBT4stY-mVY_10GPy_O0vrPrCvXaqPBQwiZtkBvgflLxRXQ"