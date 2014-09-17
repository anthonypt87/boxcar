import datetime
import mock
import unittest

from boxcar import ongoing_trip_analyzer
from boxcar.trip_analyzers import postgis_trip_analyzer
from boxcar.trip_analyzer import TripAnalyzer
from boxcar.core import domain_objects


class TripEventCreator(object):

    DEFAULT_ID = 33

    @classmethod
    def create_trip_event(
        cls,
        id=DEFAULT_ID,
        event_type=domain_objects.TripEventType.START
    ):
        return domain_objects.TripEvent(
            id=33,
            location=domain_objects.Coordinate(3, 4),
            time=datetime.datetime(2014, 2, 2),
            type=domain_objects.TripEventType.START,
        )


class TripAnalyerIntegrationTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_analyzer = \
            ongoing_trip_analyzer.OngoingTripAnalyzer()
        self._completed_trip_analyzer = \
            postgis_trip_analyzer.PostGISTripAnalyzer()
        self._analyzer = TripAnalyzer(
            self._ongoing_trip_analyzer,
            self._completed_trip_analyzer,
        )

    def test_one_ongoing_trip_in_geo_rect(self):
        trip_event = TripEventCreator.create_trip_event(
            id=1,
            event_type=domain_objects.TripEventType.START,
        )
        self._analyzer.add_trip_event_to_be_analyzed(trip_event)
        self._analyzer.get_trips_that_passed_through_geo_rect(
        )


class TripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_analyzer = mock.Mock()
        self._completed_trip_analyzer = mock.Mock()
        self._analyzer = TripAnalyzer(
            self._ongoing_trip_analyzer,
            self._completed_trip_analyzer,
        )

    def test_add_trip_start(self):
        trip_event = self._create_trip_event()
        self._analyzer.add_trip_event_to_be_analyzed(trip_event)
        self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed.assert_called_once_with(
            trip_event
        )

    def test_add_update(self):
        trip_event = self._create_trip_event(
            event_type=domain_objects.TripEventType.UPDATE
        )
        self._analyzer.add_trip_event_to_be_analyzed(trip_event)
        self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed.assert_called_once_with(
            trip_event
        )

    def _create_trip_event(
        self,
        event_type=domain_objects.TripEventType.START
    ):
        return domain_objects.TripEvent(
            id=33,
            location=domain_objects.Coordinate(3, 4),
            time=datetime.datetime(2014, 2, 2),
            type=domain_objects.TripEventType.START,
        )


if __name__ == '__main__':
    unittest.main()
