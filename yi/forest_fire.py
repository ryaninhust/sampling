from igraph import *
from random import sample,random,choice
from query import query_seed, query_single_node
from core import Algorithm

class ForestFire(Algorithm):

    def exist_edge(g, node1, node2):
        if node2 not in g.vs['name']:
            return False
        else:
            index1 = g.vs['name'].index(node1)
            index2 = g.vs['name'].index(node2)
            has_edge = g.get_eid(index1, index2, directed=False, error=False)
            if has_edge == -1:
                return False
            else:
                return True

    def update_graph(g, start_node, result):
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

    def run(self,k):
        start_seeds = [choice(self.sampled_graph.vs['name'])]
        n_attribute = len(self.sampled_graph.vertex_attributes())-2
        #all_graph = self.sampled_graph.copy()
    
        while k > 0:
            new_node = []
            if start_seeds:
                for node in start_seeds:
                    if k > 0:
                        query_result = query_single_node(node,n_attribute)
                        k = k - 1
                        unvisit = [q for q in query_result if not exist_edge(self.sampled_graph, node, q['name'])]
                        # update_graph(all_graph,node,unvisit)
                        z = sample(range(len(unvisit)),1)[0]
                        query_sample = sample(unvisit,z)
                        update_graph(self.sampled_graph,node,query_sample)
                        new_node = new_node + [n['name'] for n in query_sample]
                    else:
                        break
            else:
                start_seeds = [choice(self.sampled_graph.vs['name'])]
            start_seeds = new_node

