from igraph import *
from random import sample,random,choice
from core import Algorithm
from egraphs import FBEgoGraph
from random_walk import *

class MIRandomWalk(Algorithm):

    def update_graph(self, start_node, new_node):
        g = self.sampled_graph
        start_id = g.vs['name'].index(start_node)
        if new_node['name'] not in g.vs['name']:
            g.add_vertex(**new_node)
            index = g.vs['name'].index(new_node['name'])
            g.add_edge(start_id,index)
        else:
            index = g.vs['name'].index(new_node['name'])
            if g.get_eid(start_id, index, directed=False, error=False) == -1:
                g.add_edge(start_id,index)


    def run(self,k,m=10):
        n_attribute = len(self.sampled_graph.vertex_attributes())-2
        i = 0
        node_set = random.sample(self.sampled_graph.vs['name'],m)

        while i < k:
            query_result = self.egraph.query_node(start_node,n_attribute)
            new_node = choice(query_result)
            self.update_graph(start_node,new_node)
            '''for s in node_set:
                graph_sub = random_walk(G,s,times)
                sub_G.add_edges_from(graph_sub.edges(data=True))'''
            if random() < p_jump:
                start_node = choice(self.sampled_graph.vs['name'])
            else:
                start_node = new_node['name']
            i += 1

if __name__ == "__main__":
    fbego_graph = FBEgoGraph('data/egofb.txt')
    fuck_mirw = MIRandomWalk(fbego_graph)
    print fuck_mirw.validate()