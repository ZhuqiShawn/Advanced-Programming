# This is the baseline implemtntation, used only for testing our own implementation

import networkx as nx
import graphviz

class Graph(nx.Graph):
    def __init__(self, start=None):
        super().__init__(start)

    def __len__(self):
        return self.number_of_nodes()

    def vertices(self):
        return list(self.nodes)

    def add_vertex(self, vertex):
        return self.add_node(vertex)

    def remove_vertex(self, vertex):
        return self.remove_node(vertex)

    def get_vertex_value(self, vertex):
        if 'value' in self.nodes[vertex]:
            return self.nodes[vertex]['value']

    def set_vertex_value(self, vertex, value):
        self.nodes[vertex]['value'] = value


class WeightedGraph(Graph):

    def __init__(self, start=None):
        super().__init__(start)

    def get_weight(self, u, v):
        if 'weight' in self.edges[u, v]:
            return self.edges[u, v]['weight']

    def set_weight(self, u, v, weight):
        self.edges[u, v]['weight'] = weight


def dijkstra(graph, source, cost=lambda u, v: 1):
    def costs2attributes(G, cost, attr='weight'):
        for a, b in G.edges():
            G[a][b][attr] = cost(a, b)
    costs2attributes(graph, cost)
    return nx.shortest_path(graph, source=source, weight='weight', method='dijkstra')

def visualize(graph, view='dot', name='mygraph', nodecolors=None):
    dot = graphviz.Graph(engine=view)
    for v in graph.vertices():
        if str(v) in nodecolors:
            dot.node(str(v), style='filled', fillcolor=nodecolors[str(v)])
        else:
            dot.node(str(v))
    for a,b in graph.edges():
        dot.edge(str(a), str(b))
    dot.render(name+'.gv', view=True)


def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]
    print(path)
    colormap = {str(v): 'green' for v in path}
    visualize(G, view='dot', nodecolors=colormap)


# TEST ONLY

def demo():
    adjlist = [(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)]
    g = WeightedGraph(adjlist)
    view_shortest(g, 2, 7)

if __name__ == '__main__':
    demo()