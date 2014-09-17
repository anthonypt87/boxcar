import shapely
import shapely.wkt
import redis

from boxcar.core.adapters import WKTAdapter
from boxcar.core.domain_objects import Coordinate

r = redis.Redis('localhost')


class OngoingTripAnalyzer(object):

    def add_trip_event_to_be_analyzed(self, trip_event):
        path_id = 'trip:%s:path' % trip_event.id
        r.append(
            path_id,
            '%s %s,' % (
                trip_event.location.lat,
                trip_event.location.lng
            )
        )
        r.sadd('trip', trip_event.id)

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        rect = shapely.wkt.loads(
            WKTAdapter.convert_geo_rect_to_wkt(geo_rect)
        )
        intersected = []
        for trip_id in r.smembers('trip'):
            path_id = 'trip:%s:path' % trip_id
            points = r.get(path_id).split(',')[:-1]

            coordinates = []
            for point in points:
                coordinates.append(
                    Coordinate(*point.split(' '))
                )

            if len(coordinates) == 1:
                shape = shapely.wkt.loads(
                    WKTAdapter.convert_coordinate_to_wkt(
                        coordinates[0]
                    )
                )
            else:
                shape = shapely.wkt.loads(
                    WKTAdapter.convert_coordinates_to_linestring(
                        coordinates
                    )
                )
            if rect.intersects(
                shape
            ):
                intersected.append(trip_id)
        return len(intersected)
