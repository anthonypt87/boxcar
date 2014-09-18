import unittest

import mock
from shapely import geometry

from boxcar.trip_analyzer import ongoing_trip_analyzer
from tests import test_util


class OngoingTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_event_store = mock.Mock()
        self._analyzer = ongoing_trip_analyzer.OngoingTripAnalyzer(
            self._ongoing_trip_event_store
        )

    def test_add_trip_event_to_be_analyzed_appends_to_path(self):
        trip_event = test_util.TripEventFactory.create()
        self._analyzer.add_trip_event_to_be_analyzed(trip_event)
        self._ongoing_trip_event_store.append_to_path.assert_called_once_with(
            trip_event.id,
            trip_event.location
        )

    def test_get_trips_that_passed_through_box_uses_store(self):
        box = geometry.box(-1, -1, 1, 1)
        intersecting_linestring = geometry.LineString([(1, 0), (3, 4)])
        non_intersecting_linestring = geometry.LineString([(100, 100), (3, 4)])
        self._ongoing_trip_event_store.get_trip_id_to_paths.return_value = {
            1: intersecting_linestring,
            2: non_intersecting_linestring
        }
        self.assertEqual(
            self._analyzer.get_trips_that_passed_through_box(box),
            1
        )


if __name__ == '__main__':
    unittest.main()
