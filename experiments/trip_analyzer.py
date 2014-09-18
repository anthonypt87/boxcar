from boxcar.core.domain_objects import TripEventType


class TripAnalyzer(object):

    def __init__(self, ongoing_trip_analyzer, completed_trip_analyzer):
        self._ongoing_trip_analyzer = ongoing_trip_analyzer
        self._completed_trip_analyzer = completed_trip_analyzer

    def add_trip_event_to_be_analyzed(self, trip_event):
        if trip_event.type in (
            TripEventType.START,
            TripEventType.UPDATE
        ):
            self._ongoing_trip_analyzer.add_trip_event_to_be_analyzed(
                trip_event
            )
