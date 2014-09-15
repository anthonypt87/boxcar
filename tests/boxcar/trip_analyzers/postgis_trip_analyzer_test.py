import datetime
import unittest

import mock

from boxcar.core import db
from boxcar.core import domain_objects
from boxcar.trip_analyzers.postgis_trip_analyzer \
    import PostGISTripAnalyzer
from boxcar.trip_analyzers.postgis_trip_analyzer \
    import PostGISTripAdapter
from boxcar.trip_analyzers.postgis_trip_analyzer \
    import Trip


DEFAULT_EVENT_ID = 4
DEFAULT_FARE = 3


def create_trip(
    lat_lngs,
    event_id=DEFAULT_EVENT_ID,
    start_time=None,
    end_time=None,
    fare=DEFAULT_FARE,
):
    path = []
    for lat_lng in lat_lngs:
        path.append(domain_objects.Coordinate(*lat_lng))
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


class PostGISTripAnalyzerIntegrationTest(unittest.TestCase):

    def setUp(self):
        session = db.PSQLSession()
        session.query(Trip).delete()
        session.commit()

    def test_trips_that_passed_through_geo_rect(self):
        lat_lngs = [(1, 1), (4, 4)]
        trip = create_trip(lat_lngs)
        analyzer = PostGISTripAnalyzer()
        analyzer.add_trip(trip)
        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
            0, 0,
            3, 6
        )
        number_of_trips = \
            analyzer.get_trips_that_passed_through_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 1)

    def test_trips_that_started_or_stopped_at_geo_rect(self):
        lat_lngs = [(0, 5), (0, 0), (10, 0), (10, 5)]
        trip = create_trip(lat_lngs)

        analyzer = PostGISTripAnalyzer()
        analyzer.add_trip(trip)
        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
            9, 7,
            11, 3
        )
        number_of_trips = \
            analyzer.get_trips_started_or_stopped_in_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 1)

    def test_no_trips_stopped_or_started_in_geo_rect(self):
        lat_lngs = [(0, 5), (0, 0), (10, 0), (10, 5)]
        trip = create_trip(lat_lngs)

        analyzer = PostGISTripAnalyzer()
        analyzer.add_trip(trip)
        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
            4, -1,
            5, 10
        )
        number_of_trips = \
            analyzer.get_trips_started_or_stopped_in_geo_rect(
                geo_rect
            )
        self.assertEqual(number_of_trips, 0)

    def test_get_fares_in_started_or_stopped_in_geo_rect(self):
        paths = [
            [(0, 5), (0, 0), (10, 0), (10, 5)],
            [(10, 6), [15, 6]],
        ]

        analyzer = PostGISTripAnalyzer()
        for path in paths:
            trip = create_trip(path)
            analyzer.add_trip(trip)

        geo_rect = domain_objects.GeoRect.create_from_lat_lngs(
            11, 7,
            9, 4,
        )
        total_fares = \
            analyzer.get_fares_in_started_or_stopped_in_geo_rect(geo_rect)
        self.assertEqual(total_fares, DEFAULT_FARE * len(paths))


class PostGISTripAdapterTest(unittest.TestCase):

    def test_adapt_updates_points_and_paths(self):
        wkt_adapter = mock.Mock(
            convert_coordinate_to_wkt=mock.Mock(
                return_value='COORDINATE'
            ),
            convert_coordinates_to_linestring=mock.Mock(
                return_value='LINESTRING'
            ),
        )
        post_gis_trip_adapter = PostGISTripAdapter(
            wkt_adapter,
        )
        trip = create_trip([(1, 1)])
        db_trip = post_gis_trip_adapter.adapt(trip)
        self.assertEqual(db_trip.start_point, 'SRID=4326;COORDINATE')
        self.assertEqual(db_trip.end_point, 'SRID=4326;COORDINATE')
        self.assertEqual(db_trip.path, 'SRID=4326;LINESTRING')


if __name__ == '__main__':
    unittest.main()
