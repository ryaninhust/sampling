from igraph import Graph

from seed import generate_seed_graph


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
    name = 'egofb'

    def query_node(self, node_name, n_attribute):
        node = self.origin_graph.vs.find(name=node_name)
        return [n.attributes() for n in node.neighbors()]

    @property
    def seed_graph(self):
        if not self._seed_graph:
            self._seed_graph = generate_seed_graph(self.origin_graph, 100)
        return self._seed_graph


