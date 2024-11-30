class Credentials:

    def __init__(self, user=None, hotel=None):
        self.api_url = "https://acc2-uat-oc.hospitality-api.us-ashburn-1.ocs.oc-test.com"
        self.app_key = 'fd7dc181-d4a3-4371-a30d-835511796bc2'
        self.client_id = 'ACCORAT_Client'
        self.hotel_id = 'HB8P5'
        self.token = self._get_token()

    def _get_token(self):
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IkRXWU14cE16QlYxd3hyZ21Xa0NSWVlfRW1kTSIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb25cbiIsImlzcyI6Ind3dy5vcmFjbGUuY29tIiwib3JhY2xlLm9hdXRoLnN2Y19wX24iOiJPQXV0aFNlcnZpY2VQcm9maWxlIiwiaWF0IjoxNzMyOTk1NDY5LCJvcmFjbGUub2F1dGgucHJuLmlkX3R5cGUiOiJMREFQX1VJRCIsImV4cCI6MTczMjk5OTA2OSwib3JhY2xlLm9hdXRoLnRrX2NvbnRleHQiOiJ1c2VyX2Fzc2VydGlvbiIsImF1ZCI6WyJodHRwczovLypvcmFjbGUqLmNvbSIsImh0dHBzOi8vKi5pbnQgIiwiaHR0cHM6Ly8qb2NzLm9jLXRlc3QuY29tLyJdLCJwcm4iOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb25cbiIsImp0aSI6IjBmNjA2MmQwLTE2NTgtNDEyYy1hYzE1LWM5ZTdiZWMxOTQ2NiIsIm9yYWNsZS5vYXV0aC5jbGllbnRfb3JpZ2luX2lkIjoiQUNDT1JBVF9DbGllbnQiLCJ1c2VyLnRlbmFudC5uYW1lIjoiRGVmYXVsdERvbWFpbiIsIm9yYWNsZS5vYXV0aC5pZF9kX2lkIjoiMTIzNDU2NzgtMTIzNC0xMjM0LTEyMzQtMTIzNDU2Nzg5MDEyIn0.tr0D8gm63NNmY1qfsjWQ2YAZbUf-6lZ5wBKIBpKudv9xGBYIW81gUgsWhG9tp5uOJ8ryiTWDQlMrPI_RealMSsYeYlBiLRkbXRHdqpV-ts2mJXA4i70qFQdIf1XwV_VHrTi-2lu5XyWFEarxTkLv6RqfqJWAvJ94Bn-zx5hqygi8UV_LvjuUxmMAqHGvx3SoFtU3LvIF9_TvOtR8Litx1iKJ4JODwF8Q6FX_yW6PMB7z_f7-N1hDcGjljv4EkBvvOGtOHxvl_Uuv4gBVCb1FYUrFBA5Ys6yO_w24L1xTES_MpWfNSErRUykPekELNuXSpFQN7hcIEMaNLQ8ceL8KeA"
    
    def get_fake_cpf(hotel):
        return '99999999999'
    


# ProfId = 778553
# Reserva = confirmation 5025386 | Id 1067493
# Checkin = 13/03/2023
# Checkout = 14/03/2023



# Reservation Master = 1067493
# shareProfileId = 792915