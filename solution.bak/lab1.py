# -*- coding:utf-8 -*-

import json
import math
import re


def build_tram_stops(jsonobject):
    with open(jsonobject, 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
        stop_key = list(temp.keys())

        info_stop = dict()
        for i in stop_key:
            info_stop[i] = dict()
            info_stop[i]['lat'] = float(temp[i]['position'][0])
            info_stop[i]['lon'] = float(temp[i]['position'][1])
    return info_stop



def build_tram_lines(lines_path):
    with open(lines_path, "r", encoding='utf-8') as f:
        tram_number = []
        tram_stop = []
        tram_time = []
        for i in f:
            if len(i)==3 or len(i) ==4:
                tram_number.append(i[:-2])
                tmp = []
                tram_stop.append(tmp)

                time_tmp = []
                tram_time.append(time_tmp)

            if len(i)>6:
                tmp.append(i[:-6].rstrip())
                
                time_tmp.append(    list(map(int, (i[-6:].replace("\n", "")).split(':')))      )

        
    tram_lines = dict(zip(tram_number, tram_stop))
    tram_time = dict(zip(tram_number, tram_time))

    # The second part
    info_stop = build_tram_stops(jsonobject)

    all_stop = list( set( [j for i in tram_lines.keys() for j in tram_lines[i]] ) )
    all_stop = dict(zip(all_stop, [i for i in range(len(all_stop))]))
    stop_time = dict()

    for _stop in all_stop:
        stop_time[_stop] = {}

    for i in tram_lines.keys():
        for j in range(len(tram_lines[i])):
            if j <= (len(tram_lines[i])-2):
                tmp = dict()
                tmp[tram_lines[i][j+1]] = (tram_time[i][j+1][0] - tram_time[i][j][0])*60 + (tram_time[i][j+1][1] - tram_time[i][j][1])
                stop_time[tram_lines[i][j]].update(tmp)
            
            if j <= (len(tram_lines[i])-2):
                j = j+1
                tmp = dict()
                tmp[tram_lines[i][-j-1]] = (tram_time[i][-j][0] - tram_time[i][-j-1][0])*60 + (tram_time[i][-j][1] - tram_time[i][-j-1][1])
                stop_time[tram_lines[i][-j]].update(tmp)
    
    return tram_lines,stop_time

def build_tram_network(jsonobject, lines_path):
    info_stop = build_tram_stops(jsonobject)
    tram_lines,stop_time  = build_tram_lines(lines_path)
    tramnetwork = {'stops':info_stop, 'lines':tram_lines, 'times':stop_time}
    with open('../data/tramnetwork.json', 'w') as f:
        json.dump(tramnetwork, f)
    return tramnetwork


def lines_via_stop(tramnetwork, stop):
    for line in tramnetwork['lines'].keys():
        if stop in tramnetwork['lines'][line]:
            print('Line {} go via the {}'.format(line, stop))


def lines_between_stops(tramnetwork, stop1, stop2):
    for line in tramnetwork['lines'].keys():
        if (stop1 in tramnetwork['lines'][line]) and (stop2 in tramnetwork['lines'][line]):
            if tramnetwork['lines'][line].index(stop1) <= tramnetwork['lines'][line].index(stop2):
                print('Line {} can go from {} to {}, given direction'.format(line, stop1, stop2))
            else: 
                print('Line {} can go from {} to {}, opposite direction'.format(line, stop1, stop2))



def time_between_stops(tramnetwork, line, stop1, stop2):
    if line not in list(tramnetwork['lines'].keys()):
        print("There is not line {}. Please check your enter.".format(line))

    if stop1 not in tramnetwork['lines'][line] or stop2 not in tramnetwork['lines'][line]:
        print("You can't go from {0} to {1} or from {1} to {0} by line{2}.".format(stop1, stop2, line))
    
    stop1_index = tramnetwork['lines'][line].index(stop1)
    stop2_index = tramnetwork['lines'][line].index(stop2)


    if stop1_index <= stop2_index:
        stops = tramnetwork['lines'][line][ stop1_index : stop2_index+1]
    else: 
        stops = tramnetwork['lines'][line][ stop2_index : stop1_index+1]
    time_cost = 0
    for current_stop,next_stop in zip(stops[:-1], stops[1:]):
        time_cost += tramnetwork['times'][current_stop][next_stop]
        
    print("It costs {} minutes from {} to {} by line {}".format(time_cost, stop1, stop2, line))




def distance_between_stops(tramnetwork, stop1, stop2):
    R = 6371.009
    lat = [tramnetwork['stops'][stop1]['lat'] * math.pi/180, tramnetwork['stops'][stop2]['lat'] * math.pi/180] 
    lon = [tramnetwork['stops'][stop1]['lon'] * math.pi/180, tramnetwork['stops'][stop2]['lon'] * math.pi/180] 
    tmp = (lat[1]-lat[0])**2 + (math.cos((lat[1]+lat[0])/2) * (lon[1]-lon[0]))**2
    distance = R * math.sqrt( tmp ) * 1000
    print("The distance between {} and {} is {:.2f} m.".format(stop1, stop2, distance))






def dialogue(tramnetwork_path):

    def check_key_words(tramnetwork, key_words, re_index):
        all_stop = list(tramnetwork['stops'].keys())
        all_line = list(tramnetwork['lines'].keys())
        if re_index == 2:
            if (key_words[0] not in all_line) or (key_words[1] not in all_stop) or (key_words[2] not in all_stop):
                print("unknown arguments")
                return 1
        
        else:
            for key_word in key_words:
                if (key_word not in all_stop):
                    print("unknown arguments")
                    return 1

    with open(tramnetwork_path, 'r', encoding='utf-8') as f:
        tramnetwork = json.loads(f.read())
    
    re0 = "via (.+)"
    re1 = "between (.+) and (.+)"
    re2 = "time with (.+) from (.+) to (.+)"
    re3 = "distance from (.+) to (.+)"
    re_question = [re0, re1, re2, re3]
    
    print("Do you need help?")
    

    while True:
        usr_input = input(">")

        if usr_input=='quit':break
        
        wrong_question = 1
        for re_index, _re in enumerate(re_question):
            if re.search(_re, usr_input):
                key_words = re.findall(_re, usr_input)
                if re_index  == 0:
                    wrong_question = 0
                    if check_key_words(tramnetwork, key_words, re_index):
                        continue
                    lines_via_stop(tramnetwork, key_words[0])

                if re_index  == 1:
                    wrong_question = 0
                    if check_key_words(tramnetwork, key_words, re_index):
                        continue
                    lines_between_stops(tramnetwork, key_words[0], key_words[1])

                if re_index  == 2:
                    wrong_question = 0
                    if check_key_words(tramnetwork, key_words, re_index):
                        continue
                    time_between_stops(tramnetwork, key_words[0], key_words[1], key_words[2])

                if re_index  == 3:
                    wrong_question = 0
                    if check_key_words(tramnetwork, key_words, re_index):
                        continue
                    distance_between_stops(tramnetwork, key_words[0], key_words[1])
            
        if wrong_question:
            print("sorry, try again")


jsonobject = '../data/tramstops.json'
lines_path = '../data/tramlines.txt'
tramnetwork_path = 'C:/Users/M/Project/DAT515/DAT515_Proj/data/tramnetwork.json'

dialogue(tramnetwork_path)
