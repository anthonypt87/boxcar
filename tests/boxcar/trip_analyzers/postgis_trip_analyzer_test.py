import datetime
import unittest

from boxcar.core import db
from boxcar.core import domain_objects
from boxcar.trip_analyzers.postgis_trip_analyzer \
    import PostGISTripAnalyzer
from boxcar.trip_analyzers.postgis_trip_analyzer \
    import Trip


class PostGISTripAnalyzerIntegrationTest(unittest.TestCase):

    def setUp(self):
        session = db.Session()
        session.query(Trip).delete()

    def test_add_whole_trip_events(self):
        trip = self._create_trip()
        analyzer = PostGISTripAnalyzer()
        analyzer.add_trip(trip)
        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
            0, 0,
            3, 3
        )
        number_of_trips = \
            analyzer.get_trips_that_passed_through_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 1)

    def _create_trip(self):
        event_id = 4
        path = [
            domain_objects.Coordinate(1, 1),
            domain_objects.Coordinate(2, 2),
            domain_objects.Coordinate(3, 3),
            domain_objects.Coordinate(4, 4),
            domain_objects.Coordinate(5, 4)
        ]
        return domain_objects.Trip(
            id=event_id,
            path=path,
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            fare=4
        )


if __name__ == '__main__':
    unittest.main()
