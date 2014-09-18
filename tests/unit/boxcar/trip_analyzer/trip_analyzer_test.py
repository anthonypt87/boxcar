import datetime
import unittest

import mock

from boxcar.core import domain_objects
from boxcar.trip_analyzer import trip_analyzer
from shapely import geometry
from tests import test_util


class TripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_analyzer = mock.Mock()
        self._completed_trip_analyzer = mock.Mock()
        self._trip_analyzer = trip_analyzer.TripAnalyzer(
            self._ongoing_trip_analyzer,
            self._completed_trip_analyzer,
        )

    def test_add_trip_start_adds_to_ongoing_trip_analyzer(self):
        trip_event = self._submit_trip_event_with_type(
            domain_objects.TripEventType.START
        )
        self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed.\
            assert_called_once_with(
                trip_event
            )

    def _submit_trip_event_with_type(self, event_type):
        trip_event = test_util.TripEventFactory.create(event_type=event_type)
        self._trip_analyzer.add_trip_event_to_be_analyzed(trip_event)
        return trip_event

    def test_add_update_adds_to_ongoing_trip_analyzer(self):
        trip_event = self._submit_trip_event_with_type(
            domain_objects.TripEventType.UPDATE
        )
        self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed.\
            assert_called_once_with(
                trip_event
            )

    def tests_persists_update_when_job_is_completed(self):
        trip_event = test_util.TripEventFactory.create(
            event_type=domain_objects.TripEventType.END,
            point=geometry.Point(5, 5),
            fare=4
        )

        partial_trip = domain_objects.OngoingTrip(
            id=trip_event.id,
            path=geometry.LineString([(1, 2), (3, 4)]),
            start_time=datetime.datetime(2014, 1, 2),
            start_point=geometry.Point([4, 5])
        )
        self._ongoing_trip_analyzer.get_ongoing_trip_info.return_value = \
            partial_trip

        self._trip_analyzer.add_trip_event_to_be_analyzed(trip_event)

        expected_full_trip = domain_objects.Trip(
            id=trip_event.id,
            path=geometry.LineString([(1, 2), (3, 4), (5, 5)]),
            start_time=datetime.datetime(2014, 1, 2),
            start_point=geometry.Point([1, 2]),
            end_point=geometry.Point([5, 5]),
            end_time=trip_event.time,
            fare=trip_event.fare
        )

        args, _ = self._completed_trip_analyzer.add_trip.call_args
        trip = args[0]
        test_util.assert_trips_are_the_same(self, expected_full_trip, trip)

    def tests_get_trips_that_passed_through_box_sums_results(self):
        self._ongoing_trip_analyzer.get_trips_that_passed_through_box.return_value = 1
        self._completed_trip_analyzer.get_trips_that_passed_through_box.return_value = 2
        box = geometry.box(-1, 0, 2, 4)
        self.assertEqual(
            self._trip_analyzer.get_trips_that_passed_through_box(box),
            3
        )


if __name__ == '__main__':
    unittest.main()
