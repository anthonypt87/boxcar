# This needs to be on top to fix to geoalchemy
from boxcar.core import db

from geoalchemy import GeometryColumn
from geoalchemy import GeometryDDL
from geoalchemy import LineString
from geoalchemy import WKTSpatialElement
from geoalchemy import mysql
from sqlalchemy import Column
from sqlalchemy import Integer

from boxcar.core import adapters


class LinestringMySQLTripAnalyzer(object):

    def add_trip(self, trip):
        session = db.Session()
        trip = db.Trip(
            event_id=trip.id,
            path=adapters.convert_coordinates_to_linestring(
                trip.path
            )
        )
        session.add(trip)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = db.Session()
        box = WKTSpatialElement(adapters.convert_geo_rect_to_wkt(geo_rect))
        query = session.query(db.Trip).filter(
            box.intersects(db.Trip.path)
        )
        counts = query.count()
        session.commit()
        return counts


class Trip(db.Base):

    __tablename__ = 'whole_trip'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    path = GeometryColumn(
        LineString,
        comparator=mysql.MySQLComparator,
        nullable=False
    )


GeometryDDL(Trip.__table__)
