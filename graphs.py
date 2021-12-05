import graphviz
from queue import PriorityQueue

class Graph:
    """
    A class of undirected graphs.
    Internal representation:
        {node: {'_value': None, neighbour1: {}, neighbour2: {}, ...}, ...}
    """
    def __init__(self, start=None):
        "Start with an input list of edges or an empty graph, values are set to be None at first."
        self._adjlist = dict()
        if start:
            for a, b in start:
                self.add_edge(a,b)

    def __len__(self):
        "Return the length (number) of vertices."
        return len(self._adjlist.keys())

    def __getitem__(self, v):
        "Gives the neighbours and value (more info can be added, e.g. weight) of vertex v."
        return self._adjlist[v]
    
    def __str__(self):
        "Shows the adjacency list."
        st = [str(key)+' - '+str(self._adjlist[key]) for key in self._adjlist.keys()]
        return '\n'.join(st)

    def vertices(self):
        "Lists all vertices."
        return list(self._adjlist.keys())

    def edges(self):
        "Lists all edges in one direcion (sorted)."
        edges = set()
        for a in self._adjlist:
            for b in self._adjlist[a]:
                if b == '_value':
                    continue
                if a <= b:
                    edges.add((a, b))
                else:
                    edges.add((b, a))
        edges = list(edges)
        edges.sort(key=lambda a: (a[0], a[1]))
        return edges
    
    def add_vertex(self, a):
        "Adds a vertex if not exist."
        if a not in self._adjlist:
            self._adjlist[a] = {'_value': None}
    
    def add_edge(self, a, b):
        "Adds an edge, and the vertices if needed."
        self.add_vertex(a)
        self._adjlist[a][b] = dict()
        self.add_vertex(b)
        self._adjlist[b][a] = dict()

    def neighbours(self, v):
        "Lists all neighbours of v (sorted)."
        if v in self._adjlist:
            nbs = [vtx for vtx in self._adjlist[v].keys() if vtx != '_value']
            nbs.sort()
            return nbs
        return "{} is not in the current graph".format(v)

    def remove_edge(self, a, b):
        "Removes edge a -> b and b -> a."
        if a in self._adjlist:
            if b in self._adjlist[a]:
                del self._adjlist[a][b]
        if b in self._adjlist:
            if a in self._adjlist[b]:
                del self._adjlist[b][a]

    def remove_vertex(self, v):
        "Removes a vertex v, also the edges with this vertex."
        if v in self._adjlist:
            del self._adjlist[v]
        for vtx in self._adjlist:
            if v in self._adjlist[vtx]:
                del self._adjlist[vtx][v]

    def set_vertex_value(self, v, x):
        "Sets the value of the vertex v to be x."
        if v in self._adjlist:
            self._adjlist[v]['_value'] = x

    def get_vertex_value(self, v):
        "Returns the value of the vertex v."
        if v in self._adjlist:
            return self._adjlist[v]['_value']
        return "{} is not in the current graph".format(v)

class WeightedGraph(Graph):
    """
    A class of weighted undirected graphs.
    Internal representation:
        {node: {'_value': None, neighbour1: {'weight': None}, neighbour2: {'weight': None}...}, ...}
    """
    def __init__(self, start=None):
        "Start with an input list of edges or an empty graph, weights are set to be None at first."
        super().__init__(start)
    
    def get_weight(self, a, b):
        "Returns the weight of an edge a -> b."
        if a in self._adjlist:
            if b in self._adjlist[a]:
                if 'weight' in self._adjlist[a][b]:
                    return self._adjlist[a][b]['weight']
                return "The weight between {} and {} has not been set"
            return "Vertex {} does not have an neighbour {}".format(a,b)
        return "{} is not in the current graph".format(a)
    
    def set_weight(self, a, b, weight):
        "Sets the weight of edge a -> b."
        if a in self._adjlist and b in self._adjlist:
            if a in self._adjlist[b] and b in self._adjlist[a]:
                self._adjlist[a][b]['weight'] = weight
                self._adjlist[b][a]['weight'] = weight


def dijkstra(graph, source, cost=lambda u,v: 1):
    """A function to calculate shortest path from the source to all the other vertices. 

    Args:
        graph (Graph): an input Graph
        source (string): starting vertex
        cost (function, optional): the cost function used to calculate the cost between two vertices. Defaults is 1.

    Returns:
        dict: a dictionary where the keys are all target vertices reachable from the source, 
              and their values are paths from the source to the target
    """
    dist = {vtx: float('inf') for vtx in graph.vertices()}
    prev = {vtx: None for vtx in graph.vertices() if vtx != source}
    dist[source] = 0
    visted_vtx = list()
    pq = PriorityQueue()
    pq.put((dist[source], source))
    # main loop
    while not pq.empty():
        _, cur_vtx = pq.get()
        visted_vtx.append(cur_vtx)
        
        for neighbor in graph.neighbours(cur_vtx):
            weight = cost(cur_vtx, neighbor)
            if neighbor not in visted_vtx:
                old_cost = dist[neighbor]
                new_cost = dist[cur_vtx] + weight
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    dist[neighbor] = new_cost
                    prev[neighbor] = cur_vtx
    # build the output dictionary
    shortest_path = dict()
    for vtx in graph.vertices():
        if vtx != source:
            possible = True
            t = vtx
            path = list()
            while t != source:
                if t in prev:
                    path.append(t)
                    t = prev[t]
                else:
                    possible = False
                    break
            if possible:
                path.append(source)
                path.reverse()
                shortest_path[vtx] = path
    return shortest_path


def visualize(graph, view='dot', name='mygraph', nodecolors=None):
    """Function to visualize a graph

    Args:
        graph (Graph): the graph to be visualized
        view (str, optional): plot engine for plotting. Defaults to 'dot'.
        name (str, optional): the file name of plot to be saved. Defaults to 'mygraph'.
        nodecolors (dict, optional): colors to be added on stated nodes. Defaults to None.
    """
    dot = graphviz.Graph(engine=view)
    for v in graph.vertices():
        if nodecolors:
            if str(v) in nodecolors:
                dot.node(str(v), style='filled', fillcolor=nodecolors[str(v)])
            else:
                dot.node(str(v))
        else:
            dot.node(str(v))
    for a,b in graph.edges():
        dot.edge(str(a), str(b))
    dot.render(name+'.gv', view=True)


def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)
    if target in path:
        colormap = {str(v): 'orange' for v in path[target]}
        visualize(G, view='dot', nodecolors=colormap)
    else:
        print("No way from {} to {}".format(source, target))


# TEST ONLY

def demo():
    adjlist = [(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)]
    # adjlist = [(1,2), (3,3)]
    g = WeightedGraph(adjlist)
    # print(g)
    # visualize(g)
    view_shortest(g, 2, 7)
    # view_shortest(g, 1, 3)

if __name__ == '__main__':
    demo()