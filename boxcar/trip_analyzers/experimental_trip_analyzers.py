# Has to exist
from boxcar.core import db

from geoalchemy import WKTSpatialElement
from sqlalchemy import func

from boxcar.core import adapters


from geoalchemy import GeometryColumn
from geoalchemy import GeometryDDL
from geoalchemy import Point
from geoalchemy import mysql
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.mysql import TINYINT



class TripEvent(db.Base):
    __tablename__ = 'trip_event'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    coordinate = GeometryColumn(
        Point(2),
        comparator=mysql.MySQLComparator
    )
    time = Column(DateTime)
    type = Column(TINYINT(2), default=0)


GeometryDDL(TripEvent.__table__)


class TripAnalyzer(object):

    def add_trip(self, trip):
        pass

    def get_number_of_trips_started_or_stopped_in_geo_rect(self, geo_rect):
        pass

    def get_total_fares_for_trips_started_or_stopped_in_geo_rect(
        self,
        geo_rect
    ):
        pass

    def get_number_of_trips_at_time(self, event_time):
        pass

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        pass


# Kafka. Ordering


class LatLngTripInnoDBAnalyzer(object):
    pass


class InnoDBSpatial(object):
    pass


class ElasticSearch(object):
    pass


class InnoDBTripAnalyzer(object):

    def add_trip_events_2(self, trip_events):
        # This is too slow. We have to use sqlalchemy core to do bulk inserts.
        session = db.Session()
        for trip_event in trip_events:
            event = TripEvent(
                event_id=trip_event.id,
                coordinate=adapters.convert_coordinate_to_wkt(trip_event.location),
                time=trip_event.time,
                type=trip_event.type,
            )
            session.add(event)
        session.commit()

    def add_trip_events(self, trip_events):
        session = db.Session()
        params = []
        for trip_event in trip_events:
            params.append(
                dict(
                    event_id=trip_event.id,
                    coordinate=func.GeomFromText(
                        adapters.convert_coordinate_to_wkt(
                            trip_event.location
                        )
                    ),
                    time=trip_event.time.isoformat(),
                    type=trip_event.type
                )
            )
        session.execute(TripEvent.__table__.insert(values=params))
        session.commit()

    def add_trip_event(self, trip_event):
        session = db.Session()
        event = TripEvent(
            event_id=trip_event.id,
            coordinate=adapters.convert_coordinate_to_wkt(trip_event.location),
            time=trip_event.time,
            type=trip_event.type,
        )
        session.add(event)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = db.Session()
        box = WKTSpatialElement(adapters.convert_geo_rect_to_wkt(geo_rect))
        query = session.query(TripEvent).filter(
            box.intersects(TripEvent.coordinate)
        )
        counts = query.count()
        session.commit()
        return counts


class PostGISTripAnalzyer(object):
    pass


class MyISAMTripAnalyzer(object):
    pass


class MongoDBTripAnalyzer(object):
    pass


class CustomRTreeTripAnalyzer(object):
    pass
