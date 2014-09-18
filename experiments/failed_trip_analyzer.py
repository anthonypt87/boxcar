import redis
from rtree import index
from shapely import geometry
import shapely.wkt

from boxcar.core.adapters import WKTAdapter
from boxcar.core.domain_objects import Coordinate


r = redis.Redis('localhost')


class OngoingTripAnalyzer(object):

    def __init__(self):
        self._index = index.Rtree()

    def add_trip_event_to_be_analyzed(self, trip_event):
        bounds_key = 'trip:%s:bounds' % trip_event.id
        path_id = 'trip:%s:path' % trip_event.id
        r.append(
            path_id,
            '%s %s,' % (
                trip_event.location.lat,
                trip_event.location.lng
            )
        )
        r.sadd('trip', trip_event.id)

        bounds = r.lrange(bounds_key, 0, -1)
        bounds = map(float, bounds)
        new_point = geometry.Point(
            trip_event.location.lat,
            trip_event.location.lng
        )

        if not bounds:
            r.lpush(bounds_key, *map(float, new_point.bounds))
            self._index.insert(
                int(trip_event.id),
                new_point.bounds,
                obj=new_point
            )
        else:
            self._index.delete(
                int(trip_event.id),
                bounds
            )
            unparsed_points = r.get(path_id).split(',')[:-1]
            points = []
            for unparsed_point in unparsed_points:
                points.append(
                    map(float, unparsed_point.split(' '))
                )
            ls = shapely.geometry.LineString(points)
            self._index.insert(
                int(trip_event.id),
                ls.bounds,
                obj=ls
            )

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        points = geo_rect.get_all_points()
        minx = min([point.lat for point in points])
        miny = min([point.lng for point in points])
        maxx = max([point.lat for point in points])
        maxy = max([point.lng for point in points])
        box = shapely.geometry.box(
            minx, miny, maxx, maxy
        )
        intersected = self._index.intersection(
            box.bounds,
            objects=True
        )
        i = 0
        for thing in intersected:
            if thing.object.intersects(box):
                i += 1
        return i
