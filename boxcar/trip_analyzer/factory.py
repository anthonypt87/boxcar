from boxcar.trip_analyzer.trip_analyzer import TripAnalyzer
from boxcar.trip_analyzer.ongoing_trip_analyzer import OngoingTripAnalyzer
from boxcar.trip_analyzer.ongoing_trip_analyzer import OngoingTripEventStore

def create_trip_analyzer():
    ongoing_trip_event_store = OngoingTripEventStore()
    ongoing_analyzer = OngoingTripAnalyzer(ongoing_trip_event_store)
    return TripAnalyzer(ongoing_analyzer, None)
