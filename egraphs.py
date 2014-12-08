from igraph import Graph

from seed import generate_seed_graph
from query import query_seed


class EGraph(object):

    def __init__(self, path):
        self.path = path
        self._seed_graph = None
        self._g = None

    def query_node(self, name):
        raise NotImplementedError

    @property
    def origin_graph(self):
        if not self._g:
            g = Graph.Read_Ncol(self.path, directed=False)
            self._g = g.simplify()
        return self._g

    @property
    def seed_graph(self):
        raise NotImplementedError


class FBEgoGraph(EGraph):
    name = 'public'

    def query_node(self, node_name, n_attribute):
        node = self.origin_graph.vs.find(name=node_name)
        result = [{'name': n['name'], 'degree': n.degree()} for n in node.neighbors()]
        return result

    @property
    def seed_graph(self):
        if not self._seed_graph:
            self._seed_graph = generate_seed_graph(self.origin_graph, 100)
        return self._seed_graph

class RemoteGraph(EGraph):
    name = 'public'

    def query_node(self, node_name, n_attribute):
        node = self.origin_graph.vs.find(name=node_name)
        result = [{'name': n['name'], 'degree': n.degree()} for n in node.neighbors()]
        return result
    @property
    def seed_graph(self):
        if not self._seed_graph:
            self._seed_graph = query_seed()[0]
        return self._seed_graph

