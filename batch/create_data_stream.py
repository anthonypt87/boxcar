import argparse
import csv
import contextlib
import dateutil.parser


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


class DataStreamCreator(object):

    def create(self, input_filename, output_filename):
        input_events = self._get_input_events(input_filename)
        edited_events = self._edit_events(input_events)
        self._write_edited_events(edited_events, output_filename)

    def _get_input_events(self, input_filename):
        with open(input_filename) as csv_file:
            dict_reader = csv.DictReader(
                csv_file,
                fieldnames=['id', 'time', 'lat', 'lng'],
                delimiter='\t'
            )
            return list(dict_reader)

    def _edit_events(self, input_events):
        return EventEditor().edit(input_events)

    def _write_edited_events(
        self,
        edited_events,
        output_filename
    ):
        with open(output_filename, 'w') as output_file:
            writer = csv.DictWriter(
                output_file,
                fieldnames=['id', 'time', 'lat', 'lng', 'type'],
                delimiter='\t'
            )
            for event in edited_events:
                writer.writerow(event)


class EventEditor(object):

    def edit(self, input_events):
        self._tag_input_events_with_type(input_events)
        return self._sort_by_time(input_events)

    def _tag_input_events_with_type(self, input_events):
        current_trip_length = 0
        for i in xrange(len(input_events)):
            current_event = input_events[i]
            if i + 1 == len(input_events):
                current_event['type'] = 'end'
                continue

            next_event = input_events[i + 1]

            if current_event['id'] != next_event['id']:
                current_event['type'] = 'end'
                current_trip_length = 0
            else:
                if current_trip_length == 0:
                    current_event['type'] = 'start'
                else:
                    current_event['type'] = 'update'
                current_trip_length += 1
        return input_events

    def _sort_by_time(self, events):
        return sorted(
            events,
            key=lambda event: dateutil.parser.parse(
                event['time']
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a new data stream from uber input data'
    )
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')

    args = parser.parse_args()

    DataStreamCreator().create(args.input_filename, args.output_filename)
