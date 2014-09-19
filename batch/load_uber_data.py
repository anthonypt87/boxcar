import argparse
import contextlib
import csv
import datetime

import dateutil.parser

from boxcar.core import domain_objects
from boxcar.trip_ingestor import create_trip_ingestor
from shapely import geometry
from shapely import speedups
speedups.enable()


def get_tsv_loader(filename):
    @contextlib.contextmanager
    def _inner():
        with open(filename) as csv_file:
            yield csv.DictReader(
                csv_file,
                fieldnames=['id', 'time', 'lat', 'lng'],
                delimiter='\t'
            )
    return _inner


class UberDataLoader(object):

    DEFAULT_FARE = 10

    def __init__(self, trip_ingestor, tsv_loader):
        self._trip_ingestor = trip_ingestor
        self._tsv_loader = tsv_loader

    def load_uber_data(self):
        with self._tsv_loader() as loader:
            for row in loader:
                trip_event = self._create_trip_event_from_row(row)
                self._trip_ingestor.add_trip_event_to_be_analyzed(trip_event)

    def _create_trip_event_from_row(self, row):
        point = geometry.Point(float(row['lat']), float(row['lng']))
        if row['type'] == domain_objects.TripEventType.END:
            fare = self.DEFAULT_FARE
        else:
            fare = 0

        return domain_objects.TripEvent(
            id=int(row['id']),
            point=point,
            time=dateutil.parser.parse(row['time']),
            type=row['type'],
            fare=fare
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Dump uber tsv file to trip ingestor.'
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    ingestor = create_trip_ingestor()
    tsv_loader = get_tsv_loader(args.uber_path)

    UberDataLoader(ingestor, tsv_loader).load_uber_data()
