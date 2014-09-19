import unittest

from shapely import geometry

from boxcar.core import redis_client
from boxcar.core import domain_objects
from boxcar.trip_analyzer import ongoing_trip_analyzer
from boxcar import ongoing_trip_event_store
from tests import test_util
from boxcar.trip_ingestor import create_trip_ingestor


class OngoingTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        redis_client.client.flushdb()
        self._trip_ingestor = create_trip_ingestor()
        self._analyzer = ongoing_trip_analyzer.OngoingTripAnalyzer(
            ongoing_trip_event_store.OngoingTripEventStore()
        )

    def test_adding_trip_event_and_checking_if_it_shows_up_in_box(self):
        self._create_and_add_events_for_id(1, [[0, 0]])
        box = geometry.box(-1, -1, 1, 1)
        num_trips = self._analyzer.get_trips_that_passed_through_box(box)
        self.assertEqual(num_trips, 1)

    def _create_and_add_events_for_id(self, _id, lat_lngs):
        self._add_trip_to_be_analyzed(
            _id,
            lat_lngs[0],
            event_type=domain_objects.TripEventType.START
        )
        for lat_lng in lat_lngs[1:]:
            self._add_trip_to_be_analyzed(
                _id,
                lat_lng,
                event_type=domain_objects.TripEventType.UPDATE
            )

    def _add_trip_to_be_analyzed(self, _id, lat_lng, event_type):
        trip_event = test_util.TripEventFactory.create(
            id=_id,
            point=geometry.Point(lat_lng),
            type=event_type
        )
        self._trip_ingestor.add_trip_event_to_be_analyzed(trip_event)

    def test_trips_that_started_or_stopped_at_box(self):
        # Add trip that wont intersect
        lat_lngs = [(0, 5), (0, 0), (10, 0), (10, 5)]
        self._create_and_add_events_for_id(1, lat_lngs)

        # Add trip that will intersect
        lat_lngs = [(8, 4), (8, 5)]
        self._create_and_add_events_for_id(2, lat_lngs)

        box = geometry.box(7, 3, 11, 9)
        num_trips = self._analyzer.get_trips_started_or_stopped_in_box(box)
        self.assertEqual(num_trips, 1)


if __name__ == '__main__':
    unittest.main()
