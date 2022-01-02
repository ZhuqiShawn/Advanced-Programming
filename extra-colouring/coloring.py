import sys
sys.path.append('../')
import graphs as gr

colors = ['pink', 'lightgreen', 'lightblue', 'yellow', 'orange']

def simplyfy(graph, n=4):
    stack = list()
    while graph.vertices():
        num_vtx = len(graph.vertices())
        for vtx in graph.vertices():
            neighbours = graph.neighbours(vtx)
            if len(neighbours) < n:
                stack.append((vtx, neighbours))
                graph.remove_vertex(vtx)
        assert num_vtx != len(graph.vertices()), "Input graph cannot be simplyfied with n = {nn}".format(nn=n)
    return stack
        


def rebuild(graph, stack, colors):
    n = len(colors)
    colormap = dict()
    for vtx, nbs in stack[-1::-1]:
        graph.add_vertex(str(vtx))
        for nb in nbs:
            graph.add_edge(str(vtx), str(nb))
        idx = n-1
        color = colors[idx]
        exist_color = list()
        for neighbour in graph.neighbours(str(vtx)):
            if neighbour in colormap:
                exist_color.append(colormap[neighbour])
        while color in exist_color:
            idx -= 1
            color = colors[idx]
        colormap[str(vtx)] = color
    return colormap


def viz_color_graph(graph, colors):
    n = len(colors)
    stack = simplyfy(graph, n)
    colormap = rebuild(graph, stack, colors)
    gr.visualize(graph, nodecolors=colormap)


def demo():
    G = gr.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6),(3,7),(6,7),(7,8)])
    viz_color_graph(G, ['red', 'green', 'blue'])


if __name__ == '__main__':
    demo()
