import json
import math
import re
import sys


def build_tram_stops(jsonobject):
    """For buiding up the stop dictionary, where

    Args:
        jsonobject (json object): tramstops.json

    Returns:
        dictionary: 
            * keys are names of tram stops
            * values are dictionaries with the latitude and the longitude
    """
    stop_dict = dict()
    for stop in jsonobject.keys():
        stop_dict[stop] = dict()
        stop_dict[stop]['lat'] = float(jsonobject[stop]['position'][0])
        stop_dict[stop]['lon'] = float(jsonobject[stop]['position'][1])
    return stop_dict


def build_tram_lines(lines):
    """For buidling up the line dictionary

    Args:
        lines (a read txt file): tramlines.txt

    Returns:
        dictionary: 
            * keys are names (usually consisting of digits, but to be treated as strings)
            * values are lists of stop names, in the order in which the tram runs
    """
    line_dict = dict()
    cur_tram = None
    cur_stop = None
    for line in lines:
        line_list = line.split()
        if line_list:
            match = re.match(r'\d{0,2}:', line_list[0])
            if match and line_list[0][:-1] not in line_dict:
                cur_tram = line_list[0][:-1]
                line_dict[cur_tram] = list()
                continue
            if cur_tram:
                cur_stop = ' '.join(line_list[:-1])
                line_dict[cur_tram].append(cur_stop)
    return line_dict


def build_tram_times(lines):
    """For building up the time dictionary

    Args:
        lines (a read txt file): tramlines.txt

    Returns:
        dictionary: 
            * keys are stop names
            * values are dictionaries from stop names to numbers of minutes
    """
    time_dict = dict()
    # Initialization temp values
    cur_tram = None
    cur_stop, prev_stop = None, None
    h, m, ph, pm = 0, 0, 0, 0
    # indicating if it is reading info for a new tram line
    new_line = False
    for line in lines:
        line_list = line.split()
        if line_list:
            match = re.match(r'\d{0,2}:', line_list[0])
            if match and line_list[0][:-1] != cur_tram:
                cur_tram = line_list[0][:-1]
                new_line = True
                continue
            if new_line:
                cur_stop, prev_stop = None, None
                new_line = False
                h, m, ph, pm = 0, 0, 0, 0
            if cur_tram:
                cur_stop = ' '.join(line_list[:-1])
                if cur_stop not in time_dict:
                    time_dict[cur_stop] = dict()
                h, m = line_list[-1].split(':')
                h, m = int(h), int(m)
                if prev_stop:
                    time_dict[prev_stop][cur_stop] = (h-ph)*60 + m-pm
                    time_dict[cur_stop][prev_stop] = (h-ph)*60 + m-pm
                prev_stop = cur_stop
                ph, pm = h, m
    return time_dict


def build_tram_network(transtops, tramlines):
    """Puts everything together, reads two input files and writes a third json file containing one big dictionary

    Args:
        transtops (json object): tramstops.json
        tramlines (a read txt file): tramlines.txt
    """
    with open(transtops, 'r', encoding='utf-8') as jfile:
        jsonobject = json.load(jfile)
    with open(tramlines, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    stop_dict = build_tram_stops(jsonobject)
    line_dict = build_tram_lines(lines)
    time_dict = build_tram_times(lines)

    output_dict = {'stops': stop_dict, 'lines': line_dict, 'times': time_dict}
    
    with open('tramnetwork.json', 'w') as jfile:
        json.dump(output_dict, jfile, indent=4)


def line_exist(tramdict, line):
    """Check if the request line exist

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        line (string): quired line

    Returns:
        bool: if the request line exist
    """
    return line in tramdict['lines']


def stop_exist(tramdict, stop):
    """Check if the request stop exist

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        line (string): quired stop

    Returns:
        bool: if the request stop exist
    """
    return stop in tramdict['stops']


def lines_via_stop(tramdict, stop):
    """A query function that lists the lines that go via the given stop

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        stop (string): requested stop name

    Returns:
        list: a list of lines that go via the given stop
    """
    if not stop_exist(tramdict, stop):
        return "unknown arguments"
    line_dict = tramdict['lines']
    lines = [line for line in line_dict if stop in line_dict[line]]
    lines.sort(key=lambda a: int(a))
    return lines


def lines_between_stops(tramdict, stop1, stop2): 
    """A query function that lists the lines that go from stop1 to stop2

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        stop1 (string): first requested stop name
        stop2 (string): second requested stop name (should be different from stop1)

    Returns:
        list: a list of lines that go from stop1 to stop2
    """
    if not stop_exist(tramdict, stop1) or not stop_exist(tramdict, stop2):
        return "unknown arguments"
    if stop1 == stop2:
        return("Please enter two different stops!")
    line_dict = tramdict['lines']
    lines = [line for line in line_dict if stop1 in line_dict[line] and stop2 in line_dict[line]]
    lines.sort(key=lambda a: int(a))
    return lines


def time_between_stops(tramdict, line, stop1, stop2):
    """A query function that calculates the time from stop1 to stop2 along the given line

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        line (string): a tram line number
        stop1 (string): first requested stop name
        stop2 (string): second requested stop name (should be different from stop1)

    Returns:
        int: time bwteen two stops along given line
    """
    if not line_exist(tramdict, line):
        return "unknown arguments"
    if not stop_exist(tramdict, stop1) or not stop_exist(tramdict, stop2):
        return "unknown arguments"
    if stop1 == stop2:
        return("Please enter two different stops!")
    line_dict = tramdict['lines']
    time_dict = tramdict['times']
    time = 0
    index1 = line_dict[line].index(stop1)
    index2 = line_dict[line].index(stop2)
    if index1 < index2:
        stops = line_dict[line][index1:index2+1]
    else:
        l = len(line_dict[line])
        stops = line_dict[line][index1-l:index2-l-1:-1]
    stop = stops[0]
    for next_stop in stops[1:]:
        time += time_dict[stop][next_stop]
        stop = next_stop
    return time


def distance_between_stops(tramdict, stop1, stop2):
    """A query function that calculates the geographic distance between any two stops, based on their latitude and longitude

    Args:
        tramdict (dictionary): generated comprehensive dictionary stored in tramnetwork.json
        stop1 (string): first requested stop name
        stop2 (string): second requested stop name (should be different from stop1)

    Returns:
        float: the geographic distance between any two stops (unit: Km, round to 3 digits)
    """
    if not stop_exist(tramdict, stop1) or not stop_exist(tramdict, stop2):
        return "unknown arguments"
    if stop1 == stop2:
        return("Please enter two different stops!")
    stop_dict = tramdict['stops']
    Earth_Radius = 6371.009
    one_degree = math.pi/180
    lat1 = stop_dict[stop1]['lat'] * one_degree
    lon1 = stop_dict[stop1]['lon'] * one_degree
    lat2 = stop_dict[stop2]['lat'] * one_degree
    lon2 = stop_dict[stop2]['lon'] * one_degree

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    lat_m = (lat1 + lat2)/2

    distance = Earth_Radius * math.sqrt(dlat**2 + (math.cos(lat_m) * dlon)**2)
    return round(distance, 3)


def dialogue(jsonfile):
    with open(jsonfile, 'r') as jfile:
        tramdict = json.load(jfile)
    while(1):
        query = input("> ")
        if query == 'quit':
            break
        answer = answer_query(tramdict, query)
        print(answer)


def answer_query(tramdict, query):
    
    def pack_args(func_num, args_messy):
        if func_num == 0:
            return (None, args_messy, None)
        elif func_num == 1 or func_num == 3:
            return (None, args_messy[0], args_messy[1])
        else:
            return args_messy
    
    def request_for_func(func_num, line=None, stop1=None, stop2=None):
        funcs = {
            0: lines_via_stop,
            1: lines_between_stops,
            2: time_between_stops,
            3: distance_between_stops
        }
        args_format = {
            0: [stop1],
            1: [stop1, stop2],
            2: [line, stop1, stop2],
            3: [stop1, stop2]
        }
        func = funcs.get(func_num, "Invalid Function request")
        args = args_format.get(func_num, "Invalid Argument request")
        return func(tramdict, *args)
    
    re0 = r"via (.+)"
    re1 = r"between (.+) and (.+)"
    re2 = r"time with (.+) from (.+) to (.+)"
    re3 = r"distance from (.+) to (.+)"
    res = [re0, re1, re2, re3]

    for i, cur_re in enumerate(res):
        match = re.match(cur_re, query)
        if match:
            arguments = re.findall(cur_re, query)
            result = request_for_func(i, *pack_args(i, *arguments))
            return result if result else "unknown arguments"
    return "sorry, try again"


if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        transtops = './data/tramstops.json'
        tramlines = './data/tramlines.txt'
        build_tram_network(transtops, tramlines)
    else:
        jsonfile = './tramnetwork.json'
        dialogue(jsonfile)