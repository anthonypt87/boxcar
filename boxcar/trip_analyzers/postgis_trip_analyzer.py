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


class PostGISTripAnalyzer(object):

    def __init__(self):
        self._trip_adapter = PostGISTripAdapter()

    def add_trip(self, core_trip):
        session = db.PSQLSession()
        trip = self._trip_adapter.adapt(core_trip)
        session.add(trip)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = db.PSQLSession()
        box = WKTAdapter.convert_geo_rect_to_wkt(geo_rect)
        query = session.query(Trip).filter(
            Trip.path.intersects(box)
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


class PostGISTripAdapter(object):

    def __init__(self, wkt_adapter=WKTAdapter):
        self._wkt_adapter = wkt_adapter

    def adapt(self, core_trip):
        path = self._get_adapted_path(core_trip.path)
        start_point = self._get_adapted_coordinate(core_trip.start_point)
        end_point = self._get_adapted_coordinate(core_trip.end_point)
        return Trip(
            event_id=core_trip.id,
            path=path,
            start_time=core_trip.start_time,
            end_time=core_trip.end_time,
            fare=core_trip.fare,
            start_point=start_point,
            end_point=end_point,
        )

    def _get_adapted_coordinate(self, coordinate):
        wkt_value = self._wkt_adapter.convert_coordinate_to_wkt(
            coordinate
        )
        return self._prefix_with_srid(wkt_value)

    def _prefix_with_srid(self, value):
        return "SRID=4326;%s" % value

    def _get_adapted_path(self, path):
        wkt_value = self._wkt_adapter.convert_coordinates_to_linestring(
            path
        )
        return self._prefix_with_srid(wkt_value)


class Trip(db.PostgresBase):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    path = Column(
        Geometry(geometry_type='LINESTRING', srid=4326, spatial_index=True)
    )
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    end_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    fare = Column(Integer)
