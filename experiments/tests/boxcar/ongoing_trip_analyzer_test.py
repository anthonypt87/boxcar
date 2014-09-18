import datetime
import unittest


from boxcar.ongoing_trip_analyzer import OngoingTripAnalyzer
from boxcar.core.domain_objects import TripEvent
from boxcar.core.domain_objects import Coordinate
from boxcar.core.domain_objects import TripEventType
from boxcar.core.domain_objects import GeoRect


class OngoingTripAnalyzerIntegrationTest(unittest.TestCase):

    def test_add_trip_and_count(self):
        trip_analyzer = OngoingTripAnalyzer()
        trip_event = self._create_trip_event()
        trip_analyzer.add_trip_event_to_be_analyzed(
            trip_event
        )
        num = trip_analyzer.get_trips_that_passed_through_geo_rect(
            GeoRect.create_from_lat_lngs(
                -1, 1,
                1, -1
            )
        )
        self.assertEqual(num, 1)

    def _create_trip_event(self):
        return TripEvent(
            id=50000,
            location=Coordinate(0.5, 0.5),
            time=datetime.datetime.now(),
            type=TripEventType.UPDATE
        )


if __name__ == '__main__':
    unittest.main()
