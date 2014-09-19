import datetime
import unittest

from shapely import geometry
from boxcar import ongoing_trip_event_store
from boxcar.core import redis_client
from tests import test_util


class OngoingTripEventStoreTest(unittest.TestCase):

    def setUp(self):
        redis_client.client.flushdb()
        self._store = ongoing_trip_event_store.OngoingTripEventStore()

    def test_can_append_to_path_and_get_trips_map(self):
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
