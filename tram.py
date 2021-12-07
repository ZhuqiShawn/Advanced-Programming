# -*- coding: UTF-8 -*-
import math
import json
import graphs as gr
import tramdata as td

class TramStop:
    '''
    Define the TramStop class

    Values: name-str: The name of stops
            lines-list: All the lines which pass this stop
            position-tuple: The position of stop (lat and lon)

    Function: add_line(line) : Add line to lines
              get_lines() : Get all lines passing this platform
              get_name() : Get the name of this stop
              get_position() : Get the position of this stop
              set_position(lat, lon) : Set position of this stop
    ''' 
    def __init__(self, name, lines = [], lat = None, lon = None):
        self._name = str(name)
        self._lines = lines
        self._position = tuple()
        self.set_position(lat, lon)

    def add_line(self, line):
        line = str(line)
        if line not in self._lines:
            self._lines.append(line)
    
    def remove_line(self, line):
        line = str(line)
        if line in self._lines:
            self._lines.remove(line)

    def get_lines(self):
        if self._lines:
            return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        if self._position:
            return self._position

    def set_position(self, lat, lon):
        if lat != None and lon != None:
            self._position = (float(lat), float(lon))


class TramLine:
    '''
    Define the TramLine class

    Values: number-str: The number of line, but transfer to str
           stops-list: All stops where line pass

    Function: get_number() : Get the number of this line
              get_stops() : Get all stops where line pass

    ''' 
    def __init__(self, num, stops):
        self._number = str(num)
        self._stops = list(stops)
    
    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


class TramNetwork(gr.WeightedGraph):
    '''
    Define the TramNetwork class

    Values: _linedict : A dictory, the key is line(str), the value is the TramLine object
            _stopdict : A dictory, the key is stop name(str), the value is the TramStop object
            _timedict : A dictory, the key is stop1 name(str), 
                       the value is dictory, key is the stop names close to stop1, the value is the time cost

    Function: all_lines(): Get all lines, return list
              all_stops(): Get all stops, return list
              extreme_positions(): pass
              geo_distance(): Get the distance between two stop, return float
              line_stop(): Get all the stops of this line, return list
              remove_lines(): Remove one line or some lines from _linedict, _timedict, also call remove_edge function
              stop_lines(): Get all the lines will stop in this stop, return list
              stop_position(): Get the position of this stop, Retrun tuple
              transition_time(a,b): Get the time cost from stop a to stop b
    ''' 
    def __init__(self, lines=None, stops=None, times=None):
        super().__init__()

        self._linedict = dict()
        if lines:
            for line in lines:
                self._linedict[str(line)] = TramLine(line, lines[line])

        self._stopdict = dict()
        if stops:
            for stop in stops:
                _tmp_stop_line = []
                for line in lines:
                    if stop in self._linedict[line].get_stops():
                        _tmp_stop_line.append(line)
                self._stopdict[str(stop)] = TramStop(stop, lines=_tmp_stop_line, lat=stops[stop]['lat'], lon=stops[stop]['lon'])

        self._timedict = dict()
        if times:
            self._timedict = times
        # Initialize weighted graph
        for stop in self.all_stops():
            self.add_vertex(stop)
        for stop1 in self._timedict:
            for stop2 in self._timedict[stop1]:
                self.add_edge(stop1, stop2)
                self.set_weight(stop1, stop2, self._timedict[stop1][stop2])
                
    
    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    def extreme_positions(self):
        pass
    
    def geo_distance(self, a, b):
        a = str(a)
        b = str(b)

        if a not in list(self._stopdict.keys()) or b not in list(self._stopdict.keys()):
            return "unknown arguments"
        if a == b:
            return("Please enter two different stops!")
        
        lat1, lon1 = self.stop_position(a)
        lat2, lon2 = self.stop_position(b)
        
        Earth_Radius = 6371.009
        one_degree = math.pi/180
        lat1 *= one_degree
        lon1 *= one_degree
        lat2 *= one_degree
        lon2 *= one_degree

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        lat_m = (lat1 + lat2)/2

        distance = Earth_Radius * math.sqrt(dlat**2 + (math.cos(lat_m) * dlon)**2)
        return round(distance, 3)

    def line_stops(self, line):
        line = str(line)
        if line in list(self._linedict.keys()):
            return self._linedict[line].get_stops()
        return("The line {} is not exist".format(line))

    def remove_lines(self, lines):
        for line in lines:
            line = str(line)
            line_stops = self.line_stops(line)
            
            # update _linedict, remove the whole line
            if line in list(self._linedict.keys()):
                del self._linedict[line]
            
            # update _stopdict, remove the line from stop's info
            for stop in line_stops:
                if line in self._stopdict[stop].get_lines():
                    self._stopdict[stop].remove_line(line)
            
            # update _timedict
            # if no other lines passing through adjacent stops in the deleting line, delete time info
            # and also delete this edge from edges
            for i, stop in enumerate(line_stops):
                delete = True
                if i == len(line_stops)-2:
                    break
                next_stop = line_stops[i+1]
                for other_line in self.all_lines():
                    other_line_stops = self.line_stops(other_line)
                    for _i, _stop in enumerate(other_line_stops):
                        if _i == len(other_line_stops)-2:
                            break
                        _next_stop = other_line_stops[_i+1]
                        if (stop == _stop and next_stop == _next_stop) or (stop == _next_stop and next_stop == _stop):
                            delete = False
                            break
                    if not delete:
                        break
                if delete:
                    self.remove_edge(stop, next_stop)
                    del self._timedict[stop][next_stop]
                    del self._timedict[next_stop][stop]
                    

    def stop_lines(self, a):
        if a in self._stopdict:
            return self._stopdict[a].get_lines()
        
    def stop_position(self, a):
        if a in self._stopdict:
            return self._stopdict[a].get_position()

    def transition_time(self, a, b):
        if a in list(self._timedict.keys()):
            if b in list(self._timedict[a].keys()):
                return self._timedict[a][b]
            return '{} and {} are not adjacent'.format(a,b)
            


def readTramNetwork(tramfile='./tramnetwork.json'):
    '''
    Define the readTramNetwork function

    Input: the path of json file

    Output: a object of tramnetwork
    ''' 
    with open(tramfile, 'r', encoding='utf-8') as jfile:
        tramnetwork = json.load(jfile)

    lines = tramnetwork['lines']
    stops = tramnetwork['stops']
    times = tramnetwork['times']

    tramnetwork =  TramNetwork(lines, stops, times)
    return tramnetwork


def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    gr.view_shortest(G, a, b, cost=lambda u, v: G.get_weight(u, v))
    

if __name__ == '__main__':
    demo()