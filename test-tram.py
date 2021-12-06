from hypothesis import given, strategies as st
import hypothesis
import tram

gener_int = st.integers(min_value=0, max_value=100)

alphabet = [chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)]
gener_strings = st.text(alphabet=alphabet, min_size=6, max_size=9)
gener_stops = st.lists(gener_strings, min_size=8, max_size=11, unique_by=lambda x: x[0])
gener_line_stops = st.dictionaries(gener_int, gener_stops, min_size=8, max_size=10)

@hypothesis.settings(max_examples=3)
@given(gener_line_stops)
def test_line(gener_line_stops):
    lines = gener_line_stops
    tramnetwork =  tram.TramNetwork(lines, {}, {}, start=None)

    assert len(lines) == len(tramnetwork._linedict)
    assert list(set([str(line) for line in lines.keys()])) == list(set(tramnetwork.all_lines()))

    all_stop1 = [stop for line in lines for stop in lines[line]]
    all_stop2 = [stop for line in tramnetwork._linedict for stop in tramnetwork._linedict[line].get_stops()]

    assert len(all_stop1) == len(all_stop2)
    for line in lines:
        assert lines[line] == tramnetwork.line_stop(line)

test_line()