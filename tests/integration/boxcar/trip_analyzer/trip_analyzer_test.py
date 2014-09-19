import unittest

from shapely import geometry

from boxcar.trip_ingestor import create_trip_ingestor
from boxcar.core import db
from boxcar.core import domain_objects
from boxcar.core import models
from boxcar.core import redis_client
from boxcar.trip_analyzer import factory
from tests import test_util


class TripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._trip_analyzer = factory.create_trip_analyzer()
        self._trip_ingestor = create_trip_ingestor()
        self._wipe_data_stores()

    def _wipe_data_stores(self):
        redis_client.client.flushdb()
        with db.session_manager() as session:
            session.query(models.TripModel).delete()

    def test_add_trip_event_and_count(self):
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(0, 0)
        )
        self._trip_ingestor.add_trip_event_to_be_analyzed(
            trip_event
        )
        box = geometry.box(-1, -1, 1, 1)
        num_trips = self._trip_analyzer.get_trips_that_passed_through_box(
            box
        )
        self.assertEqual(num_trips, 1)

    def test_add_completed_trip_event_and_count(self):
        # TODO: clean up
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(0, 0),
            id=1,
            type=domain_objects.TripEventType.START
        )
        self._trip_ingestor.add_trip_event_to_be_analyzed(
            trip_event
        )
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(3, 3),
            id=1,
            type=domain_objects.TripEventType.END
        )
        self._trip_ingestor.add_trip_event_to_be_analyzed(
            trip_event
        )
        box = geometry.box(-1, -1, 1, 1)
        num_trips = self._trip_analyzer.get_trips_that_passed_through_box(
            box
        )
        self.assertEqual(num_trips, 1)


if __name__ == '__main__':
    unittest.main()
