import csv
import sys
import numpy as np
import networkx as nx
from haversine import haversine
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

AIRPORTS_FILE = './airports.dat'
ROUTES_FILE = './routes.dat'


def mk_airportdict(AIRPORTS_FILE):
    with open(AIRPORTS_FILE, 'r', encoding='utf-8') as csvfile:
        lines = csv.reader(csvfile)
        airportdic = {}
        for line in lines:
            if line[6] != '\\N' and line[7] != '\\N':
                airportdic[line[0]] = {'Name':line[1],
                                    'Country': line[3],
                                    'IATA': line[4],
                                    'posi': (float(line[6]), float(line[7]))}
    return airportdic

def mk_routeset(ROUTES_FILE):
    routeset = {}
    filterlines = []
    with open(ROUTES_FILE, 'r', encoding='utf-8') as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if line[3] != '\\N':
                routeset[line[3]] = []
                filterlines.append(line)

        for line in filterlines:
            if line[3] != '\\N' and line[5] != '\\N':
                routeset[line[3]].append(line[5])
    return routeset



def mk_routegraph(routeset, airportdic):
    G = nx.Graph()

    all_airport = list(airportdic.keys())

    for airport in all_airport:
        G.add_node(airport , posi=airportdic[airport]['posi'])

    for start in routeset:
        for stop in routeset[start]:
            if start in all_airport and stop in all_airport:
                dis = round(haversine(airportdic[start]['posi'], airportdic[stop]['posi']), 2)
                G.add_edge(start, stop, weight = dis )
    return G


def plt_airport(G):
    lat = [G.nodes[node]['posi'][0] for node in list(G.nodes)]
    lon = [G.nodes[node]['posi'][1] for node in list(G.nodes)]

    plt.figure(figsize=(16, 10))
    plt.scatter(lon, lat, s=5, alpha = 0.7)
    plt.show()

def plt_route(G):
    lat = [G.nodes[node]['posi'][0] for node in list(G.nodes)]
    lon = [G.nodes[node]['posi'][1] for node in list(G.nodes)]

    plt.figure(figsize=(16, 10))
    plt.scatter(lon, lat, s=5, alpha = 0.7)

    for route in list(G.edges):
        lat = []
        lon = []
        for i in route:
            lat.append(G.nodes[i]['posi'][0])
            lon.append(G.nodes[i]['posi'][1])

        plt.plot(lon, lat, linewidth=0.3, alpha = 0.8)
    plt.show()


def k_spanning_tree(G, k = 1000):
    tmp = nx.algorithms.tree.mst.minimum_spanning_edges(G, algorithm='kruskal', weight='weight')
    res = [i for i in tmp][-k:]

    lat = [G.nodes[node]['posi'][0] for node in list(G.nodes)]
    lon = [G.nodes[node]['posi'][1] for node in list(G.nodes)]

    plt.figure(figsize=(16, 10))
    plt.scatter(lon, lat, s=5, alpha = 0.7)

    for line in res:
        lat = []
        lon = []
        lat.append(G.nodes[line[0]]['posi'][0])
        lat.append(G.nodes[line[1]]['posi'][0])
        lon.append(G.nodes[line[0]]['posi'][1])
        lon.append(G.nodes[line[1]]['posi'][1])

        plt.plot(lon, lat, linewidth=2, alpha = 0.8)
    plt.show()

def k_means(posi_data, k=7):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(posi_data)
    labels = kmeans.labels_
    if k<=7:
        colors = "bgrcmyk"[:k]
    if k>7:
        cmap = plt.get_cmap('viridis')
        colors = cmap(np.linspace(0, 1, k))
        
    plt.figure(figsize=(16, 10))
    for i, color in enumerate(colors):
        idx = np.where(labels==i)[0]
        plt.scatter(posi_data[idx, 1], posi_data[idx, 0], s = 2, alpha = 0.7, color = color)
    plt.show()



if __name__ == '__main__':

    airportdic = mk_airportdict(AIRPORTS_FILE)
    routeset = mk_routeset(ROUTES_FILE)
    G = mk_routegraph(routeset, airportdic)

    comm_pare = sys.argv
    if comm_pare[1] == 'airports':
        plt_airport(G)
    
    if comm_pare[1] == 'routes':
        plt_route(G)
    
    if comm_pare[1] == 'span':
        k_spanning_tree(G, k = int(comm_pare[2]))
    
    if comm_pare[1] == 'means':
        lat = [G.nodes[node]['posi'][0] for node in list(G.nodes)]
        lon = [G.nodes[node]['posi'][1] for node in list(G.nodes)]
        posi_data = np.array([lat, lon]).T
        k_means(posi_data, k = int(comm_pare[2]))
    



    

    