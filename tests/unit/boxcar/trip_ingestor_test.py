import datetime
import unittest

import mock
from shapely import geometry

from boxcar.trip_ingestor import TripIngestor
from boxcar.trip_ingestor import OngoingTripIngestor
from boxcar.core import domain_objects
from tests import test_util


class TripIngestorTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_store = mock.Mock()
        self._ongoing_trip_ingestor = mock.Mock()
        self._completed_trip_ingestor = mock.Mock()
        self._trip_ingestor = TripIngestor(
            self._ongoing_trip_ingestor,
            self._completed_trip_ingestor,
            self._ongoing_trip_store,
        )

    def test_add_trip_start_adds_to_ongoing_trip_ingestor(self):
        trip_event = self._submit_trip_event_with_type(
            domain_objects.TripEventType.START
        )
        self._ongoing_trip_ingestor.add_trip_event_to_be_analyzed.\
            assert_called_once_with(
                trip_event
            )

    def _submit_trip_event_with_type(self, event_type):
        trip_event = test_util.TripEventFactory.create(type=event_type)
        self._trip_ingestor.add_trip_event_to_be_analyzed(trip_event)
        return trip_event

    def test_add_update_adds_to_ongoing_trip_ingestor(self):
        trip_event = self._submit_trip_event_with_type(
            domain_objects.TripEventType.UPDATE
        )
        self._ongoing_trip_ingestor.add_trip_event_to_be_analyzed.\
            assert_called_once_with(
                trip_event
            )

    def tests_persists_update_when_job_is_completed_and_wipes_ongoing_row(
        self
    ):
        trip_event = test_util.TripEventFactory.create(
            type=domain_objects.TripEventType.END,
            point=geometry.Point(5, 5),
            fare=4
        )

        partial_trip = domain_objects.OngoingTrip(
            id=trip_event.id,
            path=geometry.LineString([(1, 2), (3, 4)]),
            start_time=datetime.datetime(2014, 1, 2),
            start_point=geometry.Point([4, 5])
        )
        self._ongoing_trip_store.get_ongoing_trip_info.return_value = \
            partial_trip

        self._trip_ingestor.add_trip_event_to_be_analyzed(trip_event)

        expected_full_trip = domain_objects.Trip(
            id=trip_event.id,
            path=geometry.LineString([(1, 2), (3, 4), (5, 5)]),
            start_time=datetime.datetime(2014, 1, 2),
            start_point=geometry.Point([1, 2]),
            end_point=geometry.Point([5, 5]),
            end_time=trip_event.time,
            fare=trip_event.fare
        )

        args, _ = self._completed_trip_ingestor.add_trip.call_args
        trip = args[0]
        test_util.assert_trips_are_the_same(self, expected_full_trip, trip)

        self._ongoing_trip_store.wipe_all_info.assert_called_once_with(
            trip_event.id
        )


class OngoingTripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._ongoing_trip_store = mock.Mock()
        self._ongoing_trip_ingestor = OngoingTripIngestor(
            self._ongoing_trip_store
        )

    def test_add_trip_event_to_be_analyzed_adds_info_if_start(self):
        trip_event = test_util.TripEventFactory.create(
            type=domain_objects.TripEventType.START
        )
        self._ongoing_trip_ingestor.add_trip_event_to_be_analyzed(trip_event)
        self._ongoing_trip_store.add_trip_info.\
            assert_called_once_with(
                trip_event.id,
                trip_event.point,
                trip_event.time
            )
        self._assert_append_to_path_called_correctly(trip_event)

    def _assert_append_to_path_called_correctly(self, trip_event):
        self._ongoing_trip_store.append_to_path.assert_called_once_with(
            trip_event.id,
            trip_event.point
        )

    def test_add_trip_event_to_be_analyzed_appends_to_path(self):
        trip_event = test_util.TripEventFactory.create(
            type=domain_objects.TripEventType.UPDATE
        )
        self._ongoing_trip_ingestor.add_trip_event_to_be_analyzed(trip_event)
        self.assertFalse(
            self._ongoing_trip_store.add_trip_info.called
        )
        self._assert_append_to_path_called_correctly(trip_event)


if __name__ == '__main__':
    unittest.main()
