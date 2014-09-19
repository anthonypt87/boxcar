from boxcar.ongoing_trip_store import OngoingTripStore
from boxcar.trip_analyzer.completed_trip_analyzer import CompletedTripAnalyzer
from boxcar.trip_analyzer.ongoing_trip_analyzer import OngoingTripAnalyzer
from boxcar.trip_analyzer.trip_analyzer import TripAnalyzer


def create_trip_analyzer():
    ongoing_trip_store = OngoingTripStore()
    ongoing_analyzer = OngoingTripAnalyzer(ongoing_trip_store)

    completed_trip_analyzer = CompletedTripAnalyzer()
    return TripAnalyzer(ongoing_analyzer, completed_trip_analyzer)
