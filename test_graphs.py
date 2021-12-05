from hypothesis import given, strategies as st
import hypothesis
import graphs as native
import graphs_baseline as baseline

def equal(edges1, edges2):
    edgeset1 = set([frozenset(edge) for edge in edges1])
    edgeset2 = set([frozenset(edge) for edge in edges2])
    return edgeset1 == edgeset2

# generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)

# generate list of random weights
weights_random = st.floats(min_value=10, max_value=50)

# generate pairs of small integers 
twoints = st.tuples(smallints, smallints)

# generate edges with weights
edges_with_weight = st.tuples(twoints, weights_random)

# generate lists of pairs of small integers 
# where x != y for each pair (x, y) 
st_edge_list_with_weight = st.lists(edges_with_weight, unique_by=(lambda x: x[0][0], lambda x: x[0][1]))

@hypothesis.settings(deadline=None)
@given(st_edge_list_with_weight)
def test(edges_with_weight):
    eds = list()
    weights = list()
    for entry in edges_with_weight:
        eds.append(entry[0])
        weights.append(entry[1])
    G_base = baseline.WeightedGraph(eds)
    G_native = native.WeightedGraph(eds)
    
    # Testing all vertices and edges are added
    for a, b in eds:
        assert a in G_native.vertices() and b in G_native.vertices()
        assert (a, b) in G_native.edges() or (b, a) in G_native.edges()
    
    # Testing __len__()
    assert len(G_base) == len(G_native)
    
    # Testing vertices()
    assert set(G_base.vertices()) == set(G_native.vertices())
   
    # Testing edges()
    assert equal(set(G_base.edges()), set(G_native.edges()))
    
    # Testing neighbours()
    for i in G_base.vertices():
        assert set(G_base.neighbors(i)) == set(G_native.neighbours(i))
    
    # if (a, b) is in edges(), both a and b are in vertices()
    for (a, b) in G_native.edges():
        assert a in G_native.vertices() and b in G_native.vertices()
    
    # if a has b as its neighbour, then b has a as its neighbour
    for vtx in G_native.vertices():
        for nbr in G_native.neighbours(vtx):
            assert vtx in G_native.neighbours(nbr)
    
    # the shortest path from a to b is the reverse of the shortest path from b to a 
    # (but notice that this can fail in situations where there are several shortest paths)

    # Without weights
    
    for vtx_a in G_native.vertices():
        for vtx_b in G_native.vertices():
            if vtx_a != vtx_b:
                path_a_t = baseline.dijkstra(G_base, vtx_a)
                path_b_t = baseline.dijkstra(G_base, vtx_b)
                path_a = native.dijkstra(G_native, vtx_a)
                path_b = native.dijkstra(G_native, vtx_b)
                if vtx_b in path_a:
                    if path_a[vtx_b] != path_b[vtx_a][::-1]:
                        print('Without weights: ')
                        print('a: {}\tb: {}\na->b: {}\nb->a: {}\n'.format(vtx_a, vtx_b, path_a[vtx_b], path_b[vtx_a]))

                    assert path_a_t[vtx_b] == path_a[vtx_b] or len(path_a_t[vtx_b]) == len(path_a[vtx_b])
                    assert path_b_t[vtx_a] == path_b[vtx_a] or len(path_b_t[vtx_a]) == len(path_b[vtx_a])

    # With weights
    
    for i, edge in enumerate(eds):
        a, b = edge
        w = weights[i]
        G_native.set_weight(a,b,w)
        G_base.set_weight(a,b,w)
        
    for vtx_a in G_native.vertices():
        for vtx_b in G_native.vertices():
            if vtx_a != vtx_b:
                path_a_t = baseline.dijkstra(G_base, vtx_a, cost=lambda u, v: G_base.get_weight(u,v))
                path_b_t = baseline.dijkstra(G_base, vtx_b, cost=lambda u, v: G_base.get_weight(u,v))
                path_a = native.dijkstra(G_native, vtx_a, cost=lambda u, v: G_native.get_weight(u,v))
                path_b = native.dijkstra(G_native, vtx_b, cost=lambda u, v: G_native.get_weight(u,v))
                if vtx_b in path_a:
                    if path_a[vtx_b] != path_b[vtx_a][::-1]:
                        print('With weights: ')
                        print('a: {}\tb: {}\na->b: {}\nb->a: {}\n'.format(vtx_a, vtx_b, path_a[vtx_b], path_b[vtx_a]))

                    assert path_a_t[vtx_b] == path_a[vtx_b] or len(path_a_t[vtx_b]) == len(path_a[vtx_b])
                    assert path_b_t[vtx_a] == path_b[vtx_a] or len(path_b_t[vtx_a]) == len(path_b[vtx_a])

if __name__ == '__main__':
    test()