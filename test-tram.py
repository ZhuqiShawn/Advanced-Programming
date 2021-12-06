from datetime import time
import math
from hypothesis import given, strategies as st
import hypothesis
import tram
import json

gener_int = st.integers(min_value=0, max_value=100)
alphabet = [chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)]
gener_strings = st.text(alphabet=alphabet, min_size=6, max_size=9)
gener_stops = st.lists(gener_strings, min_size=8, max_size=11, unique_by=lambda x: x[0])
gener_line_stops = st.dictionaries(gener_int, gener_stops, min_size=8, max_size=10)

@hypothesis.settings(max_examples=6)
@given(gener_line_stops)
def test_lines(gener_line_stops):
    lines = gener_line_stops
    tramnetwork =  tram.TramNetwork(lines, {}, {}, start=None)

    assert len(lines) == len(tramnetwork._linedict)
    assert list(set([str(line) for line in lines.keys()])) == list(set(tramnetwork.all_lines()))

    all_stop1 = [stop for line in lines for stop in lines[line]]
    all_stop2 = [stop for line in tramnetwork._linedict for stop in tramnetwork._linedict[line].get_stops()]

    assert len(all_stop1) == len(all_stop2)
    for line in lines:
        assert lines[line] == tramnetwork.line_stop(line)

gener_strings = st.text(alphabet=alphabet, min_size=6, max_size=9)
gener_floats = st.floats(min_value=57.6, max_value=57.9)
gener_posi = st.dictionaries(st.sampled_from(['lat','lon']), gener_floats, min_size=2, max_size=2)
gener_stops = st.dictionaries(gener_strings, gener_posi, min_size=40, max_size=50)

@hypothesis.settings(max_examples=6)
@given(gener_stops)
def test_stops(gener_stops):
    stops = gener_stops
    tramnetwork =  tram.TramNetwork({}, stops, {}, start=None)

    assert len(stops) == len(tramnetwork._stopdict)
    assert list(set([stop for stop in stops.keys()])) == list(set(tramnetwork.all_stops()))

    for stop in stops:
        assert stops[stop]['lat'] == tramnetwork.stop_position(stop)[0]
        assert stops[stop]['lon'] == tramnetwork.stop_position(stop)[1]

def connectedness_test():
    '''
    Test stop connectedness by BFS
    '''
    with open('./tramnetwork.json', 'r', encoding='utf-8') as jfile:
        tramnetwork = json.load(jfile)
    times = tramnetwork['times']
    start = list(times.keys())[0]

    queue = [start]
    all_stops = [start]
    while len(queue) > 0:
        stop = queue.pop(0)
        stops = list(times[stop].keys())
        for _stop in stops:
            if _stop not in all_stops:
                queue.append(_stop)
                all_stops.append(_stop)
    
    assert len(list(set(all_stops))) == len(list(times.keys()))
    assert set(all_stops) == set(list(times.keys()))


def main():
    test_lines()
    test_stops()
    connectedness_test()

if __name__ == '__main__':
        main()