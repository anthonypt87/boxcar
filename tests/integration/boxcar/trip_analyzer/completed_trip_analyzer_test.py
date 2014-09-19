import unittest

from shapely import geometry

from boxcar.trip_ingestor import CompletedTripIngestor
from boxcar.core import db
from boxcar.core import models
from boxcar.trip_analyzer.completed_trip_analyzer import CompletedTripAnalyzer
from tests import test_util


class CompletedTripAnalyzerIntegrationTest(unittest.TestCase):

    def setUp(self):
        with db.session_manager() as session:
            session.query(models.TripModel).delete()
        self._analyzer = CompletedTripAnalyzer()
        self._completed_trip_ingestor = CompletedTripIngestor()

    def test_trips_that_passed_through_box(self):
        lat_lngs = [(1, 1), (4, 4)]
        self._create_and_add_trip(lat_lngs)
        box = geometry.box(0, 0, 3, 6)
        number_of_trips = self._analyzer.get_trips_that_passed_through_box(box)
        self.assertEqual(number_of_trips, 1)

    def _create_and_add_trip(self, lat_lngs, **kwargs):
        trip = test_util.TripFactory.create_trip_with_lat_lngs(
            lat_lngs,
            **kwargs
        )
        self._completed_trip_ingestor.add_trip(trip)

    def test_trips_that_started_or_stopped_at_box(self):
        lat_lngs = [(0, 5), (0, 0), (10, 0), (10, 5)]
        self._create_and_add_trip(lat_lngs)
        box = geometry.box(7, 3, 11, 9)
        self._assert_number_of_trips_started_or_stopped_at(box, 1)

    def _assert_number_of_trips_started_or_stopped_at(
        self,
        box,
        expected_number_of_trips
    ):
        number_of_trips = self._analyzer.get_trips_started_or_stopped_in_box(
            box
        )
        self.assertEqual(number_of_trips, expected_number_of_trips)

    def test_no_trips_stopped_or_started_in_box(self):
        lat_lngs = [(0, 5), (0, 0), (10, 0), (10, 5)]
        self._create_and_add_trip(lat_lngs)
        box = geometry.box(4, -1, 5, 10)
        self._assert_number_of_trips_started_or_stopped_at(box, 0)

    def test_get_fares_in_started_or_stopped_in_box(self):
        paths = [
            [(0, 5), (0, 0), (10, 0), (10, 5)],
            [(10, 6), [15, 6]],
        ]

        for trip_id, path in enumerate(paths):
            self._create_and_add_trip(path, id=trip_id)

        box = geometry.box(9, 4, 11, 7)
        total_fares = \
            self._analyzer.get_fares_in_started_or_stopped_in_box(box)

        self.assertEqual(
            total_fares,
            test_util.TripFactory.DEFAULT_FARE * len(paths)
        )


if __name__ == '__main__':
    unittest.main()
