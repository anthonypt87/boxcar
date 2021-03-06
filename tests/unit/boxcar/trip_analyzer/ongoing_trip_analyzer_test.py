import datetime
import unittest

import mock
from shapely import geometry

from boxcar.trip_analyzer import ongoing_trip_analyzer


class OngoingTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_store = mock.Mock()
        self._analyzer = ongoing_trip_analyzer.OngoingTripAnalyzer(
            self._ongoing_trip_store
        )

    def test_get_trips_that_passed_through_box_uses_store(self):
        box = geometry.box(-1, -1, 1, 1)
        intersecting_linestring = geometry.LineString([(1, 0), (3, 4)])
        non_intersecting_linestring = geometry.LineString([(100, 100), (3, 4)])
        self._ongoing_trip_store.get_trip_id_to_paths.return_value = {
            1: intersecting_linestring,
            2: non_intersecting_linestring
        }
        self.assertEqual(
            self._analyzer.get_trips_that_passed_through_box(box),
            1
        )

    def test_get_trips_that_started_or_stopped_in_box(self):
        self._ongoing_trip_store.get_all_trip_info.return_value = {
            1: {
                'time': datetime.datetime(2014, 1, 1),
                'start_point': geometry.Point(0, 0)
            }
        }
        box = geometry.box(-1, -1, 1, 1)
        self.assertEqual(
            self._analyzer.get_trips_started_or_stopped_in_box(box),
            1
        )


if __name__ == '__main__':
    unittest.main()
