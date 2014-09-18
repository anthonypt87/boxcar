import datetime

from shapely import geometry

from boxcar.core import domain_objects


class TripEventFactory(object):

    @classmethod
    def create(
        self,
        location=None,
        event_type=domain_objects.TripEventType.START,
        fare=0
    ):
        location = location or geometry.Point(3, 3)
        return domain_objects.TripEvent(
            id=33,
            location=location,
            time=datetime.datetime(2014, 2, 2),
            type=event_type,
            fare=fare
        )


def assert_trips_are_the_same(test_case, trip_1, trip_2):
    standard_keys = ['id', 'start_time', 'end_time', 'fare']
    for standard_key in standard_keys:
        test_case.assertEqual(
            getattr(trip_1, standard_key),
            getattr(trip_2, standard_key)
        )


def assert_shapes_are_equal(test_case, shape_1, shape_2):
    test_case.assertEqual(shape_1.coords[:], shape_2.coords[:])
    test_case.assertIsInstance(shape_1, type(shape_2))
