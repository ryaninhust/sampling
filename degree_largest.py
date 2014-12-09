from random import sample,random,choice
from core import Algorithm
from egraphs import RemoteGraph

class DegreeLargest(Algorithm):

    def update_graph(self, start_node, result):
        g = self.sampled_graph
        start_id = g.vs['name'].index(start_node)
        for node in result:
            if node['name'] not in g.vs['name']:
                g.add_vertex(**node)
                index = g.vs['name'].index(node['name'])
                g.add_edge(start_id,index)
            else:
                index = g.vs['name'].index(node['name'])
                if g.get_eid(start_id, index, directed=False, error=False) == -1:
                    g.add_edge(start_id,index)

    def degree_largest(self):
        full_degree = self.sampled_graph.vs['degree']
        sample_degree = self.sampled_graph.degree()
        difference = [x1 - x2 for (x1, x2) in zip(full_degree, sample_degree)]
        return difference.index(max(difference))

    def run(self,k):
        n_attribute = len(self.sampled_graph.vertex_attributes())-2
        i = 0

        while i < k:
            query_node = self.sampled_graph.vs['name'][self.degree_largest()]
            query_result = self.egraph.query_node(query_node,n_attribute)
            self.update_graph(query_node,query_result)
            i += 1

if __name__ == "__main__":
    fbego_graph = RemoteGraph('data/public.txt')
    fuck_dl = DegreeLargest(fbego_graph)
    print fuck_dl.validate()
