import unittest

from shapely import geometry

from boxcar.core import redis_client
from boxcar.trip_analyzer import ongoing_trip_analyzer
from tests import test_util


class OngoingTripAnalyzerTest(unittest.TestCase):

    def _wipe_data_stores(self):
        redis_client.client.flushdb()

    def test_adding_trip_event_and_checking_if_it_shows_up_in_box(self):
        analyzer = ongoing_trip_analyzer.OngoingTripAnalyzer(
            ongoing_trip_analyzer.OngoingTripEventStore()
        )
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(0, 0)
        )
        analyzer.add_trip_event_to_be_analyzed(trip_event)
        box = geometry.box(-1, -1, 1, 1)
        num_trips = analyzer.get_trips_that_passed_through_box(box)
        self.assertEqual(num_trips, 1)


class OngoingTripEventStoreTest(unittest.TestCase):

    def setUp(self):
        redis_client.client.flushdb()

    def test_can_append_to_path_and_get_trips_map(self):
        store = ongoing_trip_analyzer.OngoingTripEventStore()
        store.append_to_path(1, geometry.Point(1, 1))
        store.append_to_path(1, geometry.Point(1, 2))
        store.append_to_path(2, geometry.Point(4, 4))
        trip_id_to_paths = store.get_trip_id_to_paths()
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


if __name__ == '__main__':
    unittest.main()
