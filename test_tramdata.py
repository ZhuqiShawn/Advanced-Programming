import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_stops_in_lines(self):
        t1 = 'via Linnéplatsen'
        a1 = ['1', '2', '6']
        t2 = 'via Hjalmar Brantingsplatsen'
        a2 = ['5', '6', '10']
        t3 = 'via Brunnsparken'
        a3 = ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11']
        tests = [t1, t2, t3]
        answers = [a1, a2, a3]
        for i in range(3):
            self.assertEqual(answer_query(self.tramdict, tests[i]), answers[i])

    def test_between_two_stops(self):
        t1 = 'between Chalmers and Valand'
        a1 = ['7', '10']
        t2 = 'between Centralstationen and Brunnsparken'
        a2 = ['1', '2', '3', '4', '7', '9', '10', '11']
        t3 = 'between Kungsportsplatsen and Masthuggstorget'
        a3 = ['3']
        tests = [t1, t2, t3]
        answers = [a1, a2, a3]
        for i in range(3):
            self.assertEqual(answer_query(self.tramdict, tests[i]), answers[i])

    def test_time_between_two_stops_along_lines(self):
        t1 = 'time with 6 from Korsvägen to SKF'
        a1 = 15
        t2 = 'time with 3 from Virginsgatan to Valand'
        a2 = 16
        t3 = 'time with 13 from Hagen to Chalmers'
        a3 = 22
        tests = [t1, t2, t3]
        answers = [a1, a2, a3]
        for i in range(3):
            self.assertEqual(answer_query(self.tramdict, tests[i]), answers[i])

    def test_distance_between_two_stops(self):
        t1 = 'distance from Chalmers to Järntorget'
        a1 = 1.628
        self.assertEqual(answer_query(self.tramdict, t1), a1) 

if __name__ == '__main__':
    unittest.main()

