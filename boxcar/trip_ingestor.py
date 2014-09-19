from geoalchemy2 import WKTElement

from boxcar import lib
from boxcar.core import db
from boxcar.core import domain_objects
from boxcar.core.models import TripModel
from boxcar.ongoing_trip_store import OngoingTripStore


def create_trip_ingestor():
    ongoing_trip_store = OngoingTripStore()
    ongoing_trip_ingestor = OngoingTripIngestor(ongoing_trip_store)
    completed_trip_ingestor = CompletedTripIngestor()
    return TripIngestor(
        ongoing_trip_ingestor,
        completed_trip_ingestor,
        ongoing_trip_store
    )


class TripIngestor(object):

    ONGOING_TRIP_TYPES = set([
        domain_objects.TripEventType.START,
        domain_objects.TripEventType.UPDATE
    ])

    def __init__(
        self,
        ongoing_trip_ingestor,
        completed_trip_ingestor,
        ongoing_trip_store
    ):
        self._ongoing_trip_ingestor = ongoing_trip_ingestor
        self._ongoing_trip_store = ongoing_trip_store
        self._completed_trip_ingestor = completed_trip_ingestor

    def add_trip_event_to_be_analyzed(self, trip_event):
        if trip_event.type in self.ONGOING_TRIP_TYPES:
            self._ongoing_trip_ingestor.add_trip_event_to_be_analyzed(
                trip_event
            )
        elif trip_event.type == domain_objects.TripEventType.END:
            self._add_completed_event(trip_event)
            self._ongoing_trip_store.wipe_all_info(trip_event.id)

    def _add_completed_event(self, trip_event):
        ongoing_trip_info = \
            self._ongoing_trip_store.get_ongoing_trip_info(
                trip_event.id
            )
        merged_path = lib.get_merged_path(
            ongoing_trip_info.path,
            trip_event.point
        )
        completed_trip = domain_objects.Trip(
            id=trip_event.id,
            path=merged_path,
            start_time=ongoing_trip_info.start_time,
            end_time=trip_event.time,
            fare=trip_event.fare,
            start_point=ongoing_trip_info.start_point,
            end_point=trip_event.point
        )
        self._completed_trip_ingestor.add_trip(completed_trip)


class CompletedTripIngestor(object):

    def add_trip(self, trip):
        trip_model = self._convert_trip_to_trip_model(trip)
        with db.session_manager() as session:
            session.add(trip_model)

    def _convert_trip_to_trip_model(self, trip):
        return TripModel(
            id=trip.id,
            path=lib.convert_shape_to_wkt_element(trip.path),
            start_time=trip.start_time,
            end_time=trip.end_time,
            fare=trip.fare,
            start_point=lib.convert_shape_to_wkt_element(trip.start_point),
            end_point=lib.convert_shape_to_wkt_element(trip.end_point),
        )


class OngoingTripIngestor(object):

    def __init__(self, ongoing_trip_store):
        self._ongoing_trip_store = ongoing_trip_store

    def add_trip_event_to_be_analyzed(self, trip_event):
        if trip_event.type == domain_objects.TripEventType.START:
            self._ongoing_trip_store.add_trip_info(
                trip_event.id,
                trip_event.point,
                trip_event.time,
            )
        self._ongoing_trip_store.append_to_path(
            trip_event.id,
            trip_event.point
        )
