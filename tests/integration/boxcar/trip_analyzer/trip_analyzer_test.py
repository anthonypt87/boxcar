import unittest

from shapely import geometry

from boxcar.core import db
from boxcar.core import models
from boxcar.core import redis_client
from boxcar.trip_analyzer import factory
from tests import test_util


class TripAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self._trip_analyzer = factory.create_trip_analyzer()
        self._wipe_data_stores()

    def _wipe_data_stores(self):
        redis_client.client.flushdb()
        with db.session_manager() as session:
            session.query(models.TripModel).delete()

    def test_add_trip_event_and_count(self):
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(0, 0)
        )
        self._trip_analyzer.add_trip_event_to_be_analyzed(
            trip_event
        )
        box = geometry.box(-1, -1, 1, 1)
        num_trips = self._trip_analyzer.get_trips_that_passed_through_box(
            box
        )
        self.assertEqual(num_trips, 1)

    def test_add_completed_trip_event_and_count(self):
        trip_event = test_util.TripEventFactory.create(
            point=geometry.Point(0, 0)
        )


if __name__ == '__main__':
    unittest.main()
