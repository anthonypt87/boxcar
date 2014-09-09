from sqlalchemy import Column
from sqlalchemy import Integer

from geoalchemy2 import Geometry
from boxcar.core import adapters
from boxcar.core import db


class PostGISTripAnalyzer(object):

    def add_trip(self, trip):
        session = db.PSQLSession()
        path = adapters.convert_coordinates_to_linestring(
            trip.path
        )
        path = 'SRID=4326;%s' % path
        trip = Trip(
            event_id=trip.id,
            path=path
        )
        session.add(trip)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = db.PSQLSession()
        box = adapters.convert_geo_rect_to_wkt(geo_rect)
        query = session.query(Trip).filter(
            Trip.path.intersects(box)
        )
        counts = query.count()
        session.commit()
        raise Exception
        return counts


class Trip(db.PostgresBase):
    __tablename__ = 'whole_trip'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    path = Column(Geometry(geometry_type='LINESTRING', srid=4326))
