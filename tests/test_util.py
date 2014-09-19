import datetime

from shapely import geometry

from boxcar.core import domain_objects


class TripEventFactory(object):

    DEFAULT_POINT = geometry.Point(3, 3)
    DEFAULT_ID = 33
    DEFAULT_FARE = 0
    DEFAULT_EVENT_TYPE = domain_objects.TripEventType.START


    @classmethod
    def create(
        cls,
        id=DEFAULT_ID,
        point=DEFAULT_POINT,
        event_type=DEFAULT_EVENT_TYPE,
        fare=DEFAULT_FARE
    ):
        return domain_objects.TripEvent(
            id=id,
            point=point,
            time=datetime.datetime(2014, 2, 2),
            type=event_type,
            fare=fare
        )


class TripFactory(object):

    DEFAULT_EVENT_ID = 4
    DEFAULT_FARE = 3

    @classmethod
    def create_trip(
        cls,
        path,
        event_id=DEFAULT_EVENT_ID,
        start_time=None,
        end_time=None,
        fare=DEFAULT_FARE,
    ):
        start_time = start_time or datetime.datetime.now()
        end_time = end_time or (start_time + datetime.timedelta(minutes=20))
        return domain_objects.Trip(
            id=event_id,
            path=path,
            start_time=start_time,
            end_time=end_time,
            fare=fare,
            start_point=path[0],
            end_point=path[-1]
        )

    @classmethod
    def create_trip_with_lat_lngs(cls, lat_lngs, *args, **kwargs):
        path = geometry.LineString(paths)
        return cls.create_trip(path, *args, **kwargs)


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
