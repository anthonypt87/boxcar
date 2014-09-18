from boxcar.core import domain_objects
from boxcar import lib


class TripAnalyzer(object):

    ONGOING_TRIP_TYPES = set([
        domain_objects.TripEventType.START,
        domain_objects.TripEventType.UPDATE
    ])

    def __init__(
        self,
        ongoing_trip_analyzer,
        completed_trip_analyzer
    ):
        self._ongoing_trip_analyzer = ongoing_trip_analyzer
        self._completed_trip_analyzer = completed_trip_analyzer

    def add_trip_event_to_be_analyzed(self, trip_event):
        if trip_event.type in self.ONGOING_TRIP_TYPES:
            self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed(
                trip_event
            )
        elif trip_event.type == domain_objects.TripEventType.END:
            self._add_completed_event(trip_event)

    def _add_completed_event(self, trip_event):
        ongoing_trip_info = self._ongoing_trip_analyzer.get_ongoing_trip_info(
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
        self._completed_trip_analyzer.add_trip(completed_trip)

    def get_trips_that_passed_through_box(self, box):
        intersecting_ongoing_trips = self._ongoing_trip_analyzer.\
            get_trips_that_passed_through_box(box)
        intersecting_completed_trips = self._completed_trip_analyzer.\
            get_trips_that_passed_through_box(box)
        return intersecting_ongoing_trips + intersecting_completed_trips
