from collections import namedtuple


class TripEventType(object):
    UPDATE = 'update'
    START = 'start'
    END = 'end'


TripEvent = namedtuple('TripEvent', 'id location time type fare')

OngoingTrip = namedtuple(
    'Trip',
    'id path start_time start_point'
)

Trip = namedtuple(
    'Trip',
    'id path start_time end_time fare start_point end_point'
)
