import redis
from rtree import index
from shapely import geometry
import shapely.wkt
from shapely.ops import linemerge

from boxcar.core.adapters import WKTAdapter
from boxcar.core.domain_objects import Coordinate


from shapely import speedups
speedups.enable()
r = redis.Redis('localhost')


def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]


class OngoingTripAnalyzer(object):

    def __init__(self):
        self.id_to_path = {}

#    def add_trip_event_to_be_analyzed(self, trip_event):
#        if trip_event.id in self.id_to_path:
#            existing_path = self.id_to_path[trip_event.id]
#            points = existing_path.coords[:]
#            points.append([
#                trip_event.location.lat,
#                trip_event.location.lng
#            ])
#            self.id_to_path[trip_event.id] = geometry.LineString(points)
#        else:
#            self.id_to_path[trip_event.id] = geometry.Point(
#                trip_event.location.lat,
#                trip_event.location.lng
#            )
#
#    def get_trips_that_passed_through_geo_rect(self, geo_rect):
#        points = geo_rect.get_all_points()
#        minx = min([point.lat for point in points])
#        miny = min([point.lng for point in points])
#        maxx = max([point.lat for point in points])
#        maxy = max([point.lng for point in points])
#        box = shapely.geometry.box(minx, miny, maxx, maxy)
#        counts = 0
#        for id, path in self.id_to_path.iteritems():
#            if box.intersects(path):
#                counts += 1
#        return counts

#    def add_trip_event_to_be_analyzed(self, trip_event):
#        if trip_event.id in self.id_to_path:
#            existing_path = self.id_to_path[trip_event.id]
#            existing_path.append((
#                trip_event.location.lat,
#                trip_event.location.lng
#            ))
#        else:
#            self.id_to_path[trip_event.id] = [
#                (
#                    trip_event.location.lat,
#                    trip_event.location.lng
#                )
#            ]
#
#    def get_trips_that_passed_through_geo_rect(self, geo_rect):
#        points = geo_rect.get_all_points()
#        minx = min([point.lat for point in points])
#        miny = min([point.lng for point in points])
#        maxx = max([point.lat for point in points])
#        maxy = max([point.lng for point in points])
#        box = shapely.geometry.box(minx, miny, maxx, maxy)
#        counts = 0
#        for id, path in self.id_to_path.iteritems():
#            if len(path) == 1:
#                shape = geometry.Point(path[0])
#            else:
#                shape = geometry.LineString(path)
#            if box.intersects(shape):
#                counts += 1
#        return counts

    def add_trip_event_to_be_analyzed(self, trip_event):
        path_id = 'trip:%s:path' % trip_event.id
        r.append(
            path_id,
            '%s %s ' % (
                trip_event.location.lat,
                trip_event.location.lng
            )
        )
        r.sadd('trip', trip_event.id)

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        points = geo_rect.get_all_points()
        minx = min([point.lat for point in points])
        miny = min([point.lng for point in points])
        maxx = max([point.lat for point in points])
        maxy = max([point.lng for point in points])
        box = shapely.geometry.box(minx, miny, maxx, maxy)

        counts = 0
        trip_ids = r.smembers('trip')
        trip_id_to_paths = self._get_trip_id_to_paths(trip_ids)
        for trip_id, raw_points in trip_id_to_paths.iteritems():
            points = raw_points.split(' ')[:-1]
            points = [float(point) for point in points]
            points = chunks(points, 2)

            if len(points) == 1:
                shape = geometry.Point(points[0])
            else:
                shape = geometry.LineString(points)

            if box.intersects(shape):
                counts += 1
        return counts

    def _get_trip_id_to_paths(self, trip_ids):
        path_ids = [
            ('trip:%s:path' % trip_id) for trip_id in trip_ids
        ]
        return dict(zip(trip_ids, r.mget(path_ids)))
