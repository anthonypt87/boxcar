from geoalchemy2 import Geometry
from geoalchemy2 import WKTElement
from geoalchemy2 import functions

from boxcar.core import db
from boxcar.core.models import TripModel


class CompletedTripAnalyzer(object):

    def __init__(self):
        self._trip_adapter = DomainToModelTripAdapter()

    def add_trip(self, trip):
        trip_model = self._convert_trip_to_trip_model(trip)
        with db.session_manager() as sessoin:
            session.add(trip_model)

    def _convert_trip_to_trip_model(self, trip):
        return Trip(
            id=trip.id,
            path=self._convert_to_wkt_element(trip.path),
            start_time=trip.start_time,
            end_time=trip.end_time,
            fare=trip.fare,
            start_point=self._convert_to_wkt_element(trip.start_point),
            end_point=self._convert_to_wkt_element(trip.end_point),
        )

    def _convert_to_wkt_element(self, shape):
        return WKTElement(shape.wkt, srid=4326)

    def get_trips_that_passed_through_box(self, box):
        with db.session_manager() as sessoin:
            query = session.query(TripModel).filter(
                TripModel.path.intersects(box.wtk)
            )
            return query.count()

    def get_trips_started_or_stopped_in_box(self, box):
        with db.session_manager() as sessoin:
            query = self._get_query_for_trip_stopped_or_stopped_in_box(
                TripModel,
                session,
                box
            )
            return query.count()

    def _get_query_for_trip_stopped_or_stopped_in_box(
        self,
        column,
        session,
        box
    ):
        wkt_box = self._convert_to_wkt_element(box)
        return session.query(column).filter(
            or_(
                functions.ST_Intersects(
                    box,
                    TripModel.start_point
                ),
                functions.ST_Intersects(
                    box,
                    TripModel.end_point
                ),
            )
        )

    def get_fares_in_started_or_stopped_in_box(self, box):
        with db.session_manager() as session:
            query = self._get_query_for_trip_stopped_or_stopped_in_box(
                func.sum(TripModel.fare),
                session,
                box
            )
            return query.scalar()
