# -*- coding: UTF-8 -*-
import json
import graphs
import tramdata as td

class TramStop:
    def __init__(self, name):
        with open('./tramnetwork.json', 'r') as jfile:
            tramnetwork = json.load(jfile)
        
        self.stops_dic = tramnetwork['stops']
        self.lines_dic = tramnetwork['lines']

        self._lines = list(self.lines_dic.keys())
        self._name = name
        self._position = ()


        self._tram_stop = {}
        for stop in tramnetwork['stops'].keys():
            self._tram_stop[stop] = {}
            self._tram_stop[stop]['_position'] = (tramnetwork['stops'][stop]['lat'],tramnetwork['stops'][stop]['lon'])

            tmp_lines = [line for line in tramnetwork['lines'] if stop in tramnetwork['lines'][line]]
            self._tram_stop[stop]['_lines'] = tmp_lines.sort(key=lambda a: int(a))


    
    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)

    def get_lines(self):
        return self.lines

    def get_name(self):
        return self.lines_dic[self._name]

    def get_position(self):
        return self.stops_dic[self._name]

    def set_position(self, lat, lon):
        if self._name not in self.stops_dic.keys():
            self.stops_dic[self._name] = {}

        self.stops_dic[self._name][lat] = lat
        self.stops_dic[self._name][lon] = lon


class TramLine:
    def __init__(self, num, stops):
        self._number = ''
        self._stops = []
    
    def get_number(self):
        pass

    def get_stops(self):
        pass


class TramNetwork(graphs.WeightedGraph):

    def __init__(self):
        self._linedict = {}
        self._stopdict = {}
        self._timedict = {}

    







def main():
    pass


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