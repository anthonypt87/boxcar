from sqlalchemy import func
from boxcar.persistence_layers import innodb
from geoalchemy import WKTSpatialElement

from boxcar import util



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


class WholeTripAnalyzer(object):

    def add_trip(self, trip):
        session = innodb.Session()
        trip = innodb.Trip(
            event_id=trip.id,
            path=util.convert_coordinates_to_linestring(
                trip.path
            )
        )
        session.add(trip)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = innodb.Session()
        box = WKTSpatialElement(util.convert_geo_rect_to_wkt(geo_rect))
        query = session.query(innodb.Trip).filter(
            box.intersects(innodb.Trip.path)
        )
        counts = query.count()
        session.commit()
        return counts


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
        session = innodb.Session()
        for trip_event in trip_events:
            event = innodb.TripEvent(
                event_id=trip_event.id,
                coordinate=util.convert_coordinate_to_wkt(trip_event.location),
                time=trip_event.time,
                type=trip_event.type,
            )
            session.add(event)
        session.commit()

    def add_trip_events(self, trip_events):
        session = innodb.Session()
        params = []
        for trip_event in trip_events:
            params.append(
                dict(
                    event_id=trip_event.id,
                    coordinate=func.GeomFromText(util.convert_coordinate_to_wkt(
                        trip_event.location
                    )),
                    time=trip_event.time.isoformat(),
                    type=trip_event.type
                )
            )
        session.execute(innodb.TripEvent.__table__.insert(values=params))
        session.commit()

    def add_trip_event(self, trip_event):
        session = innodb.Session()
        event = innodb.TripEvent(
            event_id=trip_event.id,
            coordinate=util.convert_coordinate_to_wkt(trip_event.location),
            time=trip_event.time,
            type=trip_event.type,
        )
        session.add(event)
        session.commit()

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        session = innodb.Session()
        box = WKTSpatialElement(util.convert_geo_rect_to_wkt(geo_rect))
        query = session.query(innodb.TripEvent).filter(
            box.intersects(innodb.TripEvent.coordinate)
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
