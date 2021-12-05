# Advanced-Programming
This repo is for studying the course DAT515 Advanced programming in Python at Chalmers

**dat515_labs 8**:
+ Zhuqi Xiao (zhuqix@student.chalmers.se)
+ Yadong Mao (yadong@student.chalmers.se)

## Lab1
**Note**: 
- geographical distance function was implemented with just using the Math library, but the library [Haversine](https://pypi.org/project/haversine/) was used when testing our own implemented function, 
- more helper functions were implemented besides the required functions,
- in `lines_between_stops`, `time_between_stops`, and `distance_between_stops`, two request stops are checked to be not same, otherwise "Please enter two different stops!" will be returned,
- when testing for the dialogue function, expected answers were given manually, and only limited number of testing cases are given (meight be not comprehensive).

Implemented Testing Cases:
- that all tram lines listed in the original text file ``tramlines.txt`` are included in ``linedict``,
- the list of stops for each tramline is the same in ``tramlines.txt`` and ``linedict``,
- all distances are "feasible", meaning less than 20 km,
- the time from *a* to *b* is always the same as the time from *b* to *a* along the same line,
- the lines that go via the given stop returned by dialogue function are same with manually given answers,
- the lines that go from stop1 to stop2 returned by dialogue function are same with manually given answers,
- the time from `stop1` to `stop2` along the given `line` returned by dialogue function are same with manually given answers,
- the geographic distance between any two stops returned by dialogue function, based on their latitude and longitude, is same with the distance calculated by `haversine` function using the library [Haversine](https://pypi.org/project/haversine/).

## Lab2
**Note**:
- Two implementations of graphs are included, baseline one and native one. Baseline version with using `networkx` library is just for testing use. 
- The internal representation of graph class is based on one `_adjlist` dictionary, where keys are vertices and values are sub-dictionaries. In each sub-dictionary, keys are neighbours of the parent key, and values are empty sub-sub-dictionaries that can store additional attributes, e.g. weights. One special key in the sub-dictionary is named `'_value'`, which is used for storing the value of the parent vertex. One example is shown below. 
```python
_adjlist = {
    1: {'_value': None, 2: {}, 3: {}, 4: {}},
    2: {'_value': None, 1: {}},
    3: {'_value': None, 1: {}, 4: {}, 5: {}, 6: {}, 7: {}},
    4: {'_value': None, 1: {}, 3: {}},
    5: {'_value': None, 3: {}},
    6: {'_value': None, 3: {}, 7: {}},
    7: {'_value': None, 3: {}, 6: {}}
}
```
- `dijkstra` function is natively implementated based on [this Wikipedia article](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 
- `hypothesis` library is used when testing the `Graph` class.

Implemented Testing Cases:
- that all initialized vertices and edges are added,
- that the return values of functions `__len__()`, `vertices()`, `edges()`, and `neighbours()` of baseline and native implementations are same,
- that if `(a, b)` is in `edges()`, both `a` and `b` are in `vertices()`,
- that if `a` has `b` as its neighbour, then `b` has `a` as its neighbour,
- that the shortest paths calculated by baseline and native implementation are same or at least have the same cost (length here), with or without using weight as cost function,
- that the shortest path from `a` to `b` is the reverse of the shortest path from `b` to `a`, but notice that this can fail in situations where there are several shortest paths. Hence, `assert` is not applied here, instead printing out such cases for manually checking. 