from collections import namedtuple


Coordinate = namedtuple('Coordinate', 'lat lng')


TripEvent = namedtuple('TripEvent', 'id location time type')


Trip = namedtuple('Trip', 'id path')


class GeoRect(object):

    def __init__(self, coordinate_1, coordinate_2):
        self._coordinate_1 = coordinate_1
        self._coordinate_2 = coordinate_2

    @classmethod
    def create_from_lat_lngs(cls, lat_1, lng_1, lat_2, lng_2):
        coordinate_1 = Coordinate(lat_1, lng_1)
        coordinate_2 = Coordinate(lat_2, lng_2)
        return cls(coordinate_1, coordinate_2)

    def get_all_points(self):
        return [
            Coordinate(self._coordinate_1.lat, self._coordinate_1.lng),
            Coordinate(self._coordinate_1.lat, self._coordinate_2.lng),
            Coordinate(self._coordinate_2.lat, self._coordinate_1.lng),
            Coordinate(self._coordinate_2.lat, self._coordinate_2.lng)
        ]

    def __eq__(self, other_rect):
        return set(self.get_all_points()) == set(other_rect.get_all_points())
