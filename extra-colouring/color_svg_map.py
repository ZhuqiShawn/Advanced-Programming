import json
import sys
sys.path.append('../')
import graphs as gr
import coloring as co
import xml.etree.ElementTree as ET

WHITE_SVG = './data/whitemap.svg'
COUNTRY_CODES_FILE = './data/country_codes.json'
NEIGHBORS_FILE = './data/neighbors.json' 


def read_white_svg():
    tree = ET.parse(WHITE_SVG) 
    root = tree.getroot()
    eu_country_id = []
    others_country = []

    for child in root[6].iter():
        if 'class' in child.attrib:
            if 'europe' in child.attrib['class']:
                eu_country_id.append(child.attrib['id'])
        elif child.attrib['id'] == 'ru':
            for sub_child in child:
                eu_country_id.append(sub_child.attrib['id'])
        else: others_country.append(child.attrib['id'])
    country_id = [i.upper() for i in eu_country_id]
    others_country = [i.upper() for i in others_country][1:]

    return country_id, others_country




def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBORS_FILE):
    country_dic = {}

    with open(COUNTRY_CODES_FILE, 'r', encoding='utf-8') as jfile:
        country_id_obj = json.load(jfile)
    
    with open(NEIGHBORS_FILE, 'r', encoding='utf-8') as jfile:
        neighbors_obj = json.load(jfile)
    
    for country in country_id_obj:
        country_dic[country_id_obj] = {'Name': country_id_obj['Name']}

    

    return country_id_obj, neighbors_obj