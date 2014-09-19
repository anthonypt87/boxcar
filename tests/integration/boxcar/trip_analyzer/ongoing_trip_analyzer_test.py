import datetime
import unittest

from shapely import geometry

from boxcar.core import redis_client
from boxcar.core import domain_objects
from boxcar.trip_analyzer import ongoing_trip_analyzer
from tests import test_util


class OngoingTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        redis_client.client.flushdb()
        self._analyzer = ongoing_trip_analyzer.OngoingTripAnalyzer(
            ongoing_trip_analyzer.OngoingTripEventStore()
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
        self._analyzer.add_trip_event_to_be_analyzed(trip_event)

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


class OngoingTripEventStoreTest(unittest.TestCase):

    def setUp(self):
        redis_client.client.flushdb()
        self._store = ongoing_trip_analyzer.OngoingTripEventStore()

    def test_can_append_to_path_and_get_trips_map(self):
        self._store = ongoing_trip_analyzer.OngoingTripEventStore()
        self._store.append_to_path(1, geometry.Point(1, 1))
        self._store.append_to_path(1, geometry.Point(1, 2))
        self._store.append_to_path(2, geometry.Point(4, 4))
        trip_id_to_paths = self._store.get_trip_id_to_paths()
        self._assert_trip_id_paths_same(
            trip_id_to_paths,
            {
                1: geometry.LineString([(1, 1), (1, 2)]),
                2: geometry.Point([(4, 4)])
            }
        )

    def _assert_trip_id_paths_same(
        self,
        trip_id_to_paths,
        expected_trip_id_to_paths
    ):
        self.assertEqual(len(trip_id_to_paths), len(expected_trip_id_to_paths))
        for trip_id, path in trip_id_to_paths.iteritems():
            self.assertEqual(
                path.xy,
                expected_trip_id_to_paths[trip_id].xy
            )

    def test_get_all_trip_info(self):
        self._store = ongoing_trip_analyzer.OngoingTripEventStore()

        trip_id = 1
        point = geometry.Point(1, 1)
        trip_time = datetime.datetime(2014, 1, 1)
        self._store.add_trip_info(trip_id, point, trip_time)

        id_to_trip_info = self._store.get_all_trip_info()
        trip_info = id_to_trip_info[trip_id]

        test_util.assert_shapes_are_equal(
            self,
            trip_info['start_point'],
            point
        )
        self.assertEqual(trip_info['start_time'], trip_time)


if __name__ == '__main__':
    unittest.main()
