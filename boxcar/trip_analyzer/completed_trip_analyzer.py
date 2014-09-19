from geoalchemy2 import WKTElement
from geoalchemy2 import functions
from sqlalchemy import or_
from sqlalchemy import func

from boxcar.core import db
from boxcar.core.models import TripModel


class CompletedTripAnalyzer(object):

    def _convert_to_wkt_element(self, shape):
        return WKTElement(shape.wkt, srid=4326)

    def get_trips_that_passed_through_box(self, box):
        with db.session_manager() as session:
            query = session.query(TripModel).filter(
                TripModel.path.intersects(box.wkt)
            )
            return query.count()

    def get_trips_started_or_stopped_in_box(self, box):
        with db.session_manager() as session:
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
                    wkt_box,
                    TripModel.start_point
                ),
                functions.ST_Intersects(
                    wkt_box,
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
