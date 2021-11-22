import unittest
from tramdata import *
from haversine import haversine

TRAM_FILE = './tramnetwork.json'
TRAMSTOPS_FILE = './data/tramstops.json'
TRAMLINES_FILE = './data/tramlines.txt'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']
            self.timedict = self.tramdict['times']
        with open(TRAMSTOPS_FILE, 'r') as jfile:
            self.transtops = json.load(jfile)
        with open(TRAMLINES_FILE, 'r') as f:
            self.tramlines = f.readlines()

    # Tests for dictionary building

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_lines_exist(self):
        lineset = set()
        for line in self.tramlines:
            line_list = line.split()
            if line_list:
                cur_line = re.findall(r'(\d{0,2}):', line_list[0])
                if cur_line:
                    lineset.add(*cur_line)
        for line in lineset:
            self.assertIn(line, self.linedict, msg = line + ' not in linedict')

    def test_stops_in_linedict(self):
        line_dict = dict()
        cur_tram = None
        for line in self.tramlines:
            line_list = line.split()
            if line_list:
                match = re.match(r'\d{0,2}:', line_list[0])
                if match and line_list[0][:-1] not in line_dict:
                    tram_line = re.findall(r'(\d{0,2}):', line_list[0])
                    cur_tram = tram_line[0]
                    line_dict[cur_tram] = list()
                    continue
                if cur_tram:
                    line_dict[cur_tram].append(' '.join(line_list[:-1]))
        self.assertEqual(line_dict, self.linedict)
                    
                    
    def test_distance_feasible(self):
        threshold = 20
        stops = list(self.stopdict.keys())
        msg = 'Distance between {} and {} is {}'
        for i in range(len(stops)):
            for j in range(i + 1, len(stops)):
                stop1 = stops[i]
                stop2 = stops[j]
                dist = distance_between_stops(self.tramdict, stop1, stop2)
                self.assertTrue(dist < threshold, msg = msg.format(stop1, stop2, dist)) 

    def test_time_equals(self):
        stops = list(self.timedict.keys())
        for stop in stops:
            sub_stops = list(self.timedict[stop].keys())
            for sub_stop in sub_stops:
                a2b = self.timedict[stop][sub_stop]
                b2a = self.timedict[sub_stop][stop]
                self.assertEqual(a2b, b2a)

    # Tests for the dialogue

    def test_stops_in_lines(self):
        query = "via {}"
        tests = [
            'Linnéplatsen', 
            'Hjalmar Brantingsplatsen', 
            'Brunnsparken', 
            'abcdefg' # Unknown stops
        ]
        answers = [
            ['1', '2', '6'],
            ['5', '6', '10'],
            ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11'],
            'unknown arguments'
        ]
        for i in range(len(tests)):
            self.assertEqual(answer_query(self.tramdict, query.format(tests[i])), answers[i])

    def test_between_two_stops(self):
        query = "between {} and {}"
        tests = [
            ('Chalmers', 'Valand'),
            ('Centralstationen', 'Brunnsparken'),
            ('Kungsportsplatsen', 'Masthuggstorget'),
            ('Korsvägen', 'Korsvägen'), # Same begining and ending stops
            ('abcdefg', 'Korsvägen') # Unknown stops
        ]
        answers = [
            ['7', '10'],
            ['1', '2', '3', '4', '7', '9', '10', '11'],
            ['3'],
            'Please enter two different stops!',
            'unknown arguments'
        ]
        for i in range(len(tests)):
            self.assertEqual(answer_query(self.tramdict, query.format(*tests[i])), answers[i])

    def test_time_between_two_stops_along_lines(self):
        query = "time with {} from {} to {}"
        tests = [
            ('6', 'Korsvägen', 'SKF'),
            ('6', 'SKF', 'Korsvägen'), # flipped direction
            ('3', 'Virginsgatan', 'Valand'),
            ('13', 'Hagen', 'Chalmers'),
            ('2', 'Liseberg Södra', 'Liseberg Södra'), # Same begining and ending stops
            ('80', 'Liseberg Södra', 'Valand'), # Unknown lines
            ('4', 'Angered Centrum', 'abcdef'), # Unknown stops
            ('9', 'Doktor Sydows Gata Centrum', 'Kungssten'), # Unreachable destination
        ]
        answers = [
            15, 
            15,
            16,
            22,
            'Please enter two different stops!',
            'unknown arguments',
            'unknown arguments',
            'unknown arguments'
        ]
        for i in range(len(tests)):
            self.assertEqual(answer_query(self.tramdict, query.format(*tests[i])), answers[i])

    def test_distance_between_two_stops(self):
        query = "distance from {} to {}"
        tests = [
            ('Chalmers', 'Järntorget'),
            ('Järntorget', 'Chalmers'),
            ('SKF', 'Korsvägen'),
            ('Virginsgatan', 'Valand'),
            ('Hagen', 'Chalmers'),
            ('Liseberg Södra', 'Liseberg Södra'), # Same begining and ending stops
            ('Angered Centrum', 'abcdef'), # Unknown stops
        ]

        answers = [
            self.use_haversine_calculate_distance(*tests[0]),
            self.use_haversine_calculate_distance(*tests[1]),
            self.use_haversine_calculate_distance(*tests[2]),
            self.use_haversine_calculate_distance(*tests[3]),
            self.use_haversine_calculate_distance(*tests[4]),
            'Please enter two different stops!',
            'unknown arguments'
        ]
        for i in range(len(tests)):
            self.assertEqual(answer_query(self.tramdict, query.format(*tests[i])), answers[i])
    
    def use_haversine_calculate_distance(self, stop1, stop2):
        """using Haversine library to check our own distance-calculation function

        Args:
            stop1 (string): first requested stop name
            stop2 (string): second requested stop name (should be different from stop1)

        Returns:
            float: the geographic distance between any two stops (unit: Km, round to 3 digits)
        """
        lat1 = self.stopdict[stop1]['lat']
        lon1 = self.stopdict[stop1]['lon']
        lat2 = self.stopdict[stop2]['lat']
        lon2 = self.stopdict[stop2]['lon']
        return round(haversine((lat1, lon1), (lat2, lon2)), 3)


if __name__ == '__main__':
    unittest.main()
