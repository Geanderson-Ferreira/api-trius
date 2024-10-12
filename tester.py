from src.ohip_reservations import Reservas
from src.credentials import Credentials


consulta = Reservas(Credentials('H5519'))
consulta.get_reservations_by_checkout_date('2024-10-12')
consulta.find_reservation_inside_of_results()
