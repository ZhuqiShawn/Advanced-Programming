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
