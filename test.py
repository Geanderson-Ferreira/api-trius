from src.ohip_reservations import create_share
from src.credentials import Credentials


# profile 3932931
# resvModel = 6828484

credentials = Credentials('HH', 'H9087')

r = create_share(credentials, '6828484', '3932931')


# print(r)