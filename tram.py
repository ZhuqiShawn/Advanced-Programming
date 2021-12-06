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
    def __init__(self, name, lines = [], lat = 0, lon = 0):
        self._name = str(name)
        self._lines = lines
        self.set_position( lat, lon)

    def add_line(self, line):
        line = str(line)
        if line not in self._lines:
            self._lines.append(line)

    def get_lines(self):
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = (float(lat), float(lon))


class TramLine:
    '''
    Define the TramLine class

    Values: number-str: The number of line, but transfer to str
           stops-list: All stops where line pass

    Function: get_number() : Get the number of this line
              get_stops() : Get all stops where line pass

    ''' 
    def __init__(self, num, stops = []):
        self._number = str(num)
        self._stops = stops
    
    def get_number(self):
        return self._number

    def get_stops(self):
        return list(self._stops)



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
    def __init__(self, lines, stops, times, start):
        super().__init__(start)

        self._linedict = {}
        if lines:
            for line in lines:
                self._linedict[str(line)] = TramLine(line, lines[line])


        self._stopdict = {}
        if stops:
            for stop in stops:

                _tmp_stop_line = []
                for line in lines:
                    if stop in self._linedict[line].get_stops():
                        _tmp_stop_line.append(line)
                
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
        lat1 = self._stopdict[a].get_position()[0] * one_degree
        lon1 = self._stopdict[a].get_position()[1] * one_degree
        lat2 = self._stopdict[b].get_position()[0] * one_degree
        lon2 = self._stopdict[b].get_position()[1] * one_degree

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        lat_m = (lat1 + lat2)/2

        distance = Earth_Radius * math.sqrt(dlat**2 + (math.cos(lat_m) * dlon)**2)
        return round(distance, 3)

    def line_stop(self, line):
        line = str(line)
        if line in list(self._linedict.keys()):
            return self._linedict[line].get_stops()
        return("The line {} is not exist".format(line))



    def remove_lines(self, lines):
        lines = str(lines).split(" ")

        for line in lines:
            if line in list(self._linedict.keys()):
                del self._linedict[line]
            
            line_stops = self._linedict[line]._stops
            for i in range(len(line_stops)):
                if line_stops[i] in list(self._timedict.keys()):
                    if line_stops[i+1] in list(self._timedict[line_stops[i]].keys):
                        del self._timedict[line_stops[i]][line_stops[i+1]]
                        self.remove_edge(line_stops[i], line_stops[i+1])
            
            line_stops = line_stops[::-1]
            for i in range(len(line_stops)):
                if line_stops[i] in list(self._timedict.keys()):
                    if line_stops[i+1] in list(self._timedict[line_stops[i]].keys):
                        del self._timedict[line_stops[i]][line_stops[i+1]]
                        self.remove_edge(line_stops[i], line_stops[i+1])
            
            for stop in self._stopdict:
                if line in self._stopdict[stop]._lines:
                    del self._stopdict._lines[stop][line]
            

    def stop_lines(self, a):
        if a:
            if a in self._stopdict:
                return self._stopdict[a].get_lines()
        

    def stop_position(self, a):
        if a:
            if a in self._stopdict:
                return self._stopdict[a].get_position()

    def transition_time(self, a, b):
        if a and b:
            if a in list(self._timedict.keys()):
                if b in list(self._timedict[a].keys()):
                    return 'The transition times between {} and {} is {}}'.format(a,b,self._timedict[a][b])
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

    tramnetwork =  TramNetwork(lines, stops, times, start=None)
    if times:
        for stop1 in times:
            for stop2 in times[stop1]:
                tramnetwork.add_edge(stop1, stop2)
                tramnetwork.set_weight(stop1, stop2, times[stop1][stop2])
    return tramnetwork


def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    gr.view_shortest(G, a, b)

if __name__ == '__main__':
        demo()