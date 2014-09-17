import shapely.wkt
from shapely import geometry
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.types import DateTime

from geoalchemy2 import Geometry
from geoalchemy2 import WKTElement
from geoalchemy2 import functions
from boxcar.core import db
from boxcar.core.adapters import WKTAdapter


class OngoingTripAnalyzer(object):

    def __init__(self):
        self._adapter = Adapter()

    def add_trip_event_to_be_analyzed(self, trip_event):
        session = db.PSQLSession()
        location = geometry.Point(trip_event.location.lat, trip_event.location.lng)
        print trip_event.id
        trip = session.query(OngoingTrip).filter_by(id=trip_event.id).first()
        if trip is None:
            trip = OngoingTrip(
                id=trip_event.id,
                start_time=trip_event.time,
                start_point=self._adapter.get_adapted_coordinate(
                    trip_event.location
                ),
                path=self._adapter.get_adapted_path([trip_event.location, trip_event.location])
            )
            session.add(trip)
        else:
            session.query(OngoingTrip).update(
                {
                    'path': func.ST_AddPoint(
                        OngoingTrip.path,
                        func.ST_MakePoint(1,1)
                    )
                },
                synchronize_session=False
            )
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = db.PSQLSession()
        box = WKTAdapter.convert_geo_rect_to_wkt(geo_rect)
        import ipdb; ipdb.set_trace()
        query = session.query(OngoingTrip).filter(
            OngoingTrip.path.intersects(box)
        )
        counts = query.count()
        session.commit()
        return counts

    def get_trips_started_or_stopped_in_geo_rect(self, geo_rect):
        session = db.PSQLSession()
        query = self._get_query_for_trip_stopped_or_stopped_in_geo_rect(
            Trip,
            session,
            geo_rect
        )
        counts = query.count()
        session.commit()
        return counts

    def _get_query_for_trip_stopped_or_stopped_in_geo_rect(
        self,
        column,
        session,
        geo_rect
    ):
        box = WKTElement(
            WKTAdapter.convert_geo_rect_to_wkt(geo_rect),
            srid=4326
        )
        return session.query(column).filter(
            or_(
                functions.ST_Intersects(
                    box,
                    Trip.start_point
                ),
                functions.ST_Intersects(
                    box,
                    Trip.end_point
                ),
            )
        )

    def get_fares_in_started_or_stopped_in_geo_rect(self, geo_rect):
        session = db.PSQLSession()
        query = self._get_query_for_trip_stopped_or_stopped_in_geo_rect(
            func.sum(Trip.fare),
            session,
            geo_rect
        )
        total_fare = query.scalar()
        session.commit()
        return total_fare


class Adapter(object):

    def __init__(self, wkt_adapter=WKTAdapter):
        self._wkt_adapter = wkt_adapter

    def get_adapted_coordinate(self, coordinate):
        wkt_value = self._wkt_adapter.convert_coordinate_to_wkt(
            coordinate
        )
        return self._prefix_with_srid(wkt_value)

    def _prefix_with_srid(self, value):
        return "SRID=4326;%s" % value

    def get_adapted_path(self, path):
        wkt_value = self._wkt_adapter.convert_coordinates_to_linestring(
            path
        )
        return self._prefix_with_srid(wkt_value)


class OngoingTrip(db.PostgresBase):
    __tablename__ = 'ongoing_trip'

    id = Column(Integer, primary_key=True)
    path = Column(
        Geometry(geometry_type='LINESTRING', srid=4326, spatial_index=False)
    )
    start_time = Column(DateTime)
    start_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False)
    )
