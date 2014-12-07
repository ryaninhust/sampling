from igraph import *
from random import sample,random,choice
from query import query_seed, query_single_node
from core import Algorithm

class SnowBallSampling(Algorithm):

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

    def run(self, k, quota=10, n_start=100):
        start_seeds = sample(self.sampled_graph.vs['name'],n_start)
        wave = 1
        n_attribute = len(self.sampled_graph.vertex_attributes())-2
        #all_graph = self.sampled_graph.copy()

        while k>0:
            new_node = []
            if start_seeds:
                for node in start_seeds:
                    if k>0:
                        n_influence = sample(range(quota),1)[0]
                        if n_influence==0:
                            continue
                        else:
                            query_result = query_single_node(node,n_attribute)
                            k = k - 1
                            #update_graph(all_graph,node,query_result)
                            valid_result = [q for q in query_result if q['name'] not in self.sampled_graph.vs['name']]
                            n_influence = min(n_influence,len(valid_result))
                            # additional coupons were given only under two conditions
                            if n_influence == quota and random()<0.6**quota:
                                n_influence = min(quota*2,valid_result)
                            query_sample = sample(valid_result,n_influence)
                            update_graph(self.sampled_graph,node,query_sample)
                            new_node = new_node + [n['name'] for n in query_sample]
                    else:
                        break
            else:
                start_seeds = sample(self.sampled_graph.vs['name'],n_start)
            start_seeds = new_node
            wave = wave + 1



