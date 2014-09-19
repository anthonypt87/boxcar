import unittest

import mock

from boxcar.trip_analyzer import trip_analyzer
from shapely import geometry


class TripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_analyzer = mock.Mock()
        self._completed_trip_analyzer = mock.Mock()
        self._trip_analyzer = trip_analyzer.TripAnalyzer(
            self._ongoing_trip_analyzer,
            self._completed_trip_analyzer,
        )

    def tests_get_trips_that_passed_through_box_sums_results(self):
        self._ongoing_trip_analyzer.get_trips_that_passed_through_box.\
            return_value = 1
        self._completed_trip_analyzer.get_trips_that_passed_through_box.\
            return_value = 2
        box = geometry.box(-1, 0, 2, 4)
        self.assertEqual(
            self._trip_analyzer.get_trips_that_passed_through_box(box),
            3
        )


if __name__ == '__main__':
    unittest.main()
