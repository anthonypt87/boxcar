import datetime
import unittest

from boxcar.core import db
from boxcar.core import domain_objects
from boxcar.trip_analyzers.experimental_trip_analyzers \
    import InnoDBTripAnalyzer
from boxcar.trip_analyzers.experimental_trip_analyzers \
    import TripEvent
from boxcar.core import domain_objects


class InnoDBTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        session = db.Session()
        session.query(TripEvent).delete()
        session.query(TripEvent).filter_by(id=4).delete()
        session.commit()

    def test_add_trip_event_and_test_in_georect(self):
        trip_event = self._create_trip_event()
        analyzer = InnoDBTripAnalyzer()
        analyzer.add_trip_event(trip_event)
        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
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
        location = domain_objects.Coordinate(37.79947, -122.511635)
        event_time = datetime.datetime.now()
        event_type = 1
        return domain_objects.TripEvent(
            event_id,
            location,
            event_time,
            event_type
        )


if __name__ == '__main__':
    unittest.main()
