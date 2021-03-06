import json
import sys
sys.path.append('../')
import graphs as gr
import coloring as co
import xml.etree.ElementTree as ET

WHITEMAP_FILE = './data/whitemap.svg'
COUNTRY_CODES_FILE = './data/country_codes.json'
NEIGHBORS_FILE = './data/neighbors.json' 
COLORMAP_FILE = './colormap.svg'

def read_white_svg(WHITEMAP_FILE):
    tree = ET.parse(WHITEMAP_FILE) 
    root = tree.getroot()
    eu_country_id = []
    others_country = []

    for child in root[6]:
        if 'class' in child.attrib:
            if 'europe' in child.attrib['class']:
                eu_country_id.append(child.attrib['id'])
        elif child.attrib['id'] == 'ru':
            for sub_child in child:
                eu_country_id.append(sub_child.attrib['id'])
        else: others_country.append(child.attrib['id'])
    eu_country_id = [i.upper() for i in eu_country_id]
    others_country = [i.upper() for i in others_country][1:]

    return eu_country_id, others_country


def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBORS_FILE):
    country_dic = {}

    with open(COUNTRY_CODES_FILE, 'r', encoding='utf-8') as jfile:
        country_id_obj = json.load(jfile)
    
    with open(NEIGHBORS_FILE, 'r', encoding='utf-8') as jfile:
        neighbors_obj = json.load(jfile)
    
    for country in country_id_obj:
        country_dic[country['Code']] = {'Name': country['Name'], 'Neighbors': []}

        for neighbor in neighbors_obj:
            if neighbor['countryLabel'] == country['Name']:
                for _country in country_id_obj:
                    if neighbor['neighborLabel'] == _country['Name']:
                        country_dic[country['Code']]['Neighbors'].append(_country['Code'])
    
    for coun in country_dic:
        country_dic[coun]['Neighbors'] = list(set(country_dic[coun]['Neighbors']))
    
    del country_dic['RU']
    
    country_dic['RU-main']['Neighbors'].remove('LT')
    country_dic['RU-main']['Neighbors'].remove('PL')
    country_dic['RU-Kaliningrad']['Neighbors'] = ['LT', 'PL']

    country_dic['RU-MAIN'] = country_dic['RU-main']
    country_dic['RU-KALININGRAD'] = country_dic['RU-Kaliningrad']
    del country_dic['RU-main']
    del country_dic['RU-Kaliningrad']

    return country_dic


def get_map_colors(country_dic, eu_country_id):
    eu_neighbors = []
    for coun_code in eu_country_id:
        for neig in country_dic[coun_code]['Neighbors']:
            if neig in eu_country_id:
                eu_neighbors.append((coun_code,neig))

    coun_have_nei = list(set([i[0] for i in eu_neighbors]))
    diff_coun = list(set(eu_country_id).difference(set(coun_have_nei)))

    G = gr.Graph(eu_neighbors)
    for coun in diff_coun:
        G.add_vertex(coun)

    colors = ['red', 'green', 'blue','pink']
    stack = co.simplyfy(G, 4)
    colordict = co.rebuild(G, stack, colors)
    return colordict,eu_neighbors

def color_svg_map(colordict, others_country, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE):
    tree = ET.parse(infile) 
    root = tree.getroot()

    for child in root[6].iter():
        coun_id = child.attrib['id'].upper()
        if coun_id in colordict:
            child.attrib['style'] = child.attrib['style'].replace('white', colordict[coun_id])
        if coun_id in others_country:
            child.attrib['style'] = child.attrib['style'].replace('white', '#c0c0c0')

    new_tree = ET.ElementTree(root)
    new_tree.write(outfile, encoding='utf-8')

if __name__ == '__main__':
    eu_country_id, others_country = read_white_svg(WHITEMAP_FILE)
    country_dic = get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBORS_FILE)
    colordict,eu_neighbors = get_map_colors(country_dic, eu_country_id)
    color_svg_map(colordict, others_country, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE)
    