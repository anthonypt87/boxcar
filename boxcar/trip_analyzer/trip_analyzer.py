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

    def get_trips_that_passed_through_box(self, box):
        intersecting_ongoing_trips = self._ongoing_trip_analyzer.\
            get_trips_that_passed_through_box(box)
        intersecting_completed_trips = self._completed_trip_analyzer.\
            get_trips_that_passed_through_box(box)
        return intersecting_ongoing_trips + intersecting_completed_trips
