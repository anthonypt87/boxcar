from rtree import index
from shapely import geometry
import shapely.wkt

from boxcar.core.adapters import WKTAdapter
from boxcar.core.domain_objects import Coordinate


class OngoingTripAnalyzer(object):

    def __init__(self):
        self._index = index.Rtree('rtree')
        self._index = index.Rtree('rtree')

    def add_trip_event_to_be_analyzed(self, trip_event):
        shapely_point = geometry.Point(
            trip_event.location.lat,
            trip_event.location.lng
        )

        if trip_event
        self._index.insert(
            trip_event.id,


    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        pass
