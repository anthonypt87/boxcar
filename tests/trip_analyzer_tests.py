import datetime
import unittest

from boxcar import core
from boxcar import trip_analyzer
from boxcar.persistence_layers import innodb


class InnoDBTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        session = innodb.Session()
        session.query(
            innodb.TripEvent
        ).filter_by(id=4).delete()
        session.commit()

    def test_add_trip_event_and_test_in_georect(self):
        trip_event = self._create_trip_event()
        analyzer = trip_analyzer.InnoDBTripAnalyzer()
        analyzer.add_trip_event(trip_event)
        geo_rect = core.GeoRect.create_from_lat_lngs(
            -50, -175,
            50, 175
        )
        number_of_trips = \
            analyzer.get_trips_that_passed_through_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 1)

    def _create_trip_event(self):
        event_id = 4
        location = core.Coordinate(37.79947, -122.511635)
        event_time = datetime.datetime.now()
        event_type = 1
        return core.TripEvent(event_id, location, event_time, event_type)


class AddWholeTripAnalyzerTest(unittest.TestCase):

    def test_add_whole_trip_events(self):
        trip = self._create_trip()
        analyzer = trip_analyzer.WholeTripAnalyzer(trip)
        analyzer.add_trip_event(trip_event)
        geo_rect = core.GeoRect.create_from_lat_lngs(
            -50, -175,
            50, 175
        )
        number_of_trips = \
            analyzer.get_trips_that_passed_through_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 1)

    def _create_trip(self):
        event_id = 4
        path = [
            core.Coordinate(1, 1),
            core.Coordinate(2, 2),
            core.Coordinate(3, 3),
            core.Coordinate(4, 4),
            core.Coordinate(5, 4)
        ]
        return core.Trip(event_id, path)

if __name__ == '__main__':
    unittest.main()
