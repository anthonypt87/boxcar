import unittest

from batch import create_data_stream


class EventEditorTest(unittest.TestCase):

    def test_edit_events_tags_with_type_and_sorts_by_time(self):
        # Input events are grouped by (id, time)
        input_events = [
            {
                'id': '00001',
                'time': '2007-01-07T10:54:50+00:00',
                'lat': '37.782551',
                'lng': '-122.445368'
            },
            {
                'id': '00001',
                'time': '2007-01-07T10:54:54+00:00',
                'lat': '37.782745',
                'lng': '-122.444586'
            },
            {
                'id': '00001',
                'time': '2007-01-07T10:54:58+00:00',
                'lat': '37.782842',
                'lng': '-122.443688'
            },
            {
                'id': '00002',
                'time': '2007-01-07T10:54:55+00:00',
                'lat': '37.782842',
                'lng': '-122.443688'
            },
            {
                'id': '00002',
                'time': '2007-01-07T10:55:00+00:00',
                'lat': '37.782842',
                'lng': '-122.443688'
            },
        ]
        editor = create_data_stream.EventEditor()

        output_events = editor.edit(input_events)
        expected_events = [
            {
                'id': '00001',
                'time': '2007-01-07T10:54:50+00:00',
                'lat': '37.782551',
                'lng': '-122.445368',
                'type': 'start'
            },
            {
                'id': '00001',
                'time': '2007-01-07T10:54:54+00:00',
                'lat': '37.782745',
                'lng': '-122.444586',
                'type': 'update'
            },
            {
                'id': '00002',
                'time': '2007-01-07T10:54:55+00:00',
                'lat': '37.782842',
                'lng': '-122.443688',
                'type': 'start'
            },
            {
                'id': '00001',
                'time': '2007-01-07T10:54:58+00:00',
                'lat': '37.782842',
                'lng': '-122.443688',
                'type': 'end'
            },
            {
                'id': '00002',
                'time': '2007-01-07T10:55:00+00:00',
                'lat': '37.782842',
                'lng': '-122.443688',
                'type': 'end'
            }
        ]

        self.assertEqual(output_events, expected_events)


if __name__ == '__main__':
    unittest.main()
