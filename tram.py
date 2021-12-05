# -*- coding: UTF-8 -*-
import math
import json
import graphs
import tramdata as td

class TramStop:
    def __init__(self, name, lines = [], lat = 0, lon = 0):
        self._name = str(name)
        self._lines = lines
        self._position = (lat, lon)

    def add_line(self, line):
        line = str(line)
        if line not in self.lines:
            self.lines.append(line)

    def get_lines(self):
        return self.lines

    def get_name(self):
        return self.name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position(float(lat), float(lon))


class TramLine:
    def __init__(self, num, stops = []):
        self._number = str(num)
        self._stops = stops
    
    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops



class TramNetwork(graphs.WeightedGraph):
    def __init__(self, lines, stops, times, start=None):
        super().__init__(start=start)

        self._linedict = {}
        if lines:
            for line in lines:
                self._linedict[line] = TramLine(line, lines[line])

        self._stopdict = {}
        if stops:
            for stop in stops:
                _tmp_stop_line = []
                for line in lines:
                    if stop in stops:
                        self._stopdict[stop] = TramStop(stop, lines = _tmp_stop_line, lat = stops[stop]['lat'], lon = stops[stop]['lon'])

        self._timedict = {}
        if times:
            self._timedict = times
    
    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    def extreme_positions(self):
        pass

    # def geo_distance(self,a,b):
    #     return td.distance_between_stops(self._stopdict[a], self._stopdict[b])
    
    def geo_distance(self,a,b):
        a = str(a)
        b = str(b)

        if a not in list(self._stopdict.keys()) or str(b) not in list(self._stopdict.keys()):
            return "unknown arguments"
        if a == b:
            return("Please enter two different stops!")
        Earth_Radius = 6371.009
        one_degree = math.pi/180
        lat1 = self._stopdict[a]._position[0] * one_degree
        lon1 = self._stopdict[a]._position[1] * one_degree
        lat2 = self._stopdict[b]._position[0] * one_degree
        lon2 = self._stopdict[b]._position[1] * one_degree

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        lat_m = (lat1 + lat2)/2

        distance = Earth_Radius * math.sqrt(dlat**2 + (math.cos(lat_m) * dlon)**2)
        return round(distance, 3)

    def line_stop(self, line):
        # line = str(line)
        return (self._linedict[line].get_stops())


    def remove_lines(self, lines):
        lines = str(lines).split(" ")

        for line in lines:
            if line in list(self._linedict.keys()):
                # if the stop in this line but not in other lines, del stop object
                # for stop in self._linedict[line]._stops:
                #     stop_in_otherline = 0
                #     for _line in list(self._linedict.keys()):
                #         for _stop in self._linedict[_line]._stops:
                #             if _stop == stop:
                #                 if _line != line:
                #                     stop_in_otherline = 1
                    
                #     if stop_in_otherline:
                #         print('del {}'.format(stop))
                #         del self._stopdict[stop]
                del self._linedict[line]
            
            for stop in self._stopdict:
                if line in self._stopdict[stop]._lines:
                    del self._stopdict._lines[stop][line]


        


    def stop_lines(self, a):
        if a:
            if a in self._stopdict:
                return self._stopdict[a]._lines

    def stop_position(self, a):
        if a:
            if a in self._stopdict:
                return self._stopdict[a]._position

    def transition_time(self, a, b):
        if a and b:
            if a in list(self._timedict.keys()):
                if b in list(self._timedict[a].keys()):
                    return 'The transition times between {} and {} is {}}'.format(a,b,self._timedict[a][b])
                return '{} and {} are not adjacent'.format(a,b)
            

def readTramNetwork(tramfile='./tramnetwork.json'):
    with open(tramfile, 'r', encoding='utf-8') as jfile:
        tramnetwork = json.load(jfile)

    lines = tramnetwork['lines']
    stops = tramnetwork['stops']
    times = tramnetwork['times']

    return TramNetwork(lines, stops, times, start=None)


