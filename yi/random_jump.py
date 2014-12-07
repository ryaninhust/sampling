from igraph import *
from random import sample,random,choice
from query import query_seed, query_single_node
from core import Algorithm

class RandomJump(Algorithm):

    def update_graph(g, start_node, new_node):
        start_id = g.vs['name'].index(start_node)
        if node['name'] not in g.vs['name']:
            g.add_vertex(**node)
            index = g.vs['name'].index(node['name'])
            g.add_edge(start_id,index)
        else:
            index = g.vs['name'].index(node['name'])
            if g.get_eid(start_id, index, directed=False, error=False) == -1:
                g.add_edge(start_id,index)


    def run(self,k,p_jump=0.2):
        start_node = choice(self.sampled_graph.vs['name'])
        n_attribute = len(self.sampled_graph.vertex_attributes())-2
        i = 0

        while i < k:
            query_result = query_single_node(start_node,n_attribute)
            new_node = choice(query_result)
            update_graph(self.sampled_graph,start_node,new_node)
            if random()<p_jump: 
                start_node = choice(self.sampled_graph.vs['name'])
            else:
                start_node = new_node['name']
            i = i + 1


