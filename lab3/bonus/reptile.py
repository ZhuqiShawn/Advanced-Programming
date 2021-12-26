import json
import requests
from bs4 import BeautifulSoup

def get_gids_names(url):
    gids = []
    tram_stops = []

    req = requests.get(url)
    res = BeautifulSoup(req.text,'html.parser')

    all_section = res.find_all("section")
    for section in all_section:
        a_section = section.find_all("a")
        for a in a_section:

            gid = a.get('href').split('/')[-2]
            gids.append(gid)

            _tram_stop = a.text.replace("\r\n                                ", "").replace("\r\n", "")
            _tram_stop = _tram_stop.split(',')[0]
            tram_stops.append(_tram_stop)
    
    return gids, tram_stops


def main():
    url = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'

    gids, tram_stops = get_gids_names(url)

    stop_url = 'https://www.vasttrafik.se/reseplanering/hallplatser/'
    timetable_url = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='

    url_info = dict()

    for i in range(len(tram_stops)):
        url_info[tram_stops[i]] = {'url': stop_url+gids[i]+'/', 'timetable': timetable_url+gids[i] }
    
    with open('gid.json','w', encoding = 'utf-8') as jfile:
        json.dump(url_info, jfile) 

if __name__ == '__main__':
    main()
