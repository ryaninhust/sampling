from random import choice, randrange
from core import Algorithm
from egraphs import FBEgoGraph

class TestAlgorithm(Algorithm):

    name = "test_algorithm"

    def run(self, k):
        return


class FirstSearchAlgorithm(Algorithm):

    def __init__(self, egraph, pop_method):
        super(FirstSearchAlgorithm, self).__init__(egraph)
        self.init_queue()
        self.pop_method = getattr(self, pop_method)

    def init_queue(self):
        init_node = choice(self.sampled_graph.vs)
        node_neighours = self.egraph.query_node(init_node['name'])
        self.queue = [n for n in node_neighours
                      if n['name'] not in self.sampled_graph.vs['name']]

    def depth_first(self):
        return self.queue.pop()

    def breadth_first(self):
        return self.queue.pop(0)

    def random_first(self):
        q_len = len(self.queue)
        return self.queue.pop(randrange(0, q_len))

    def run(self, k):
        for t in range(k):
            node = self.pop_method()
            self.sampled_graph.add_vertex(**node)
            node_id = self.sampled_graph.vs.find(name=node['name'])
            node_neighours = self.egraph.query_node(node['name'])
            for i in node_neighours:
                if i['name'] in self.sampled_graph.vs['name']:
                    neighbor_id = self.sampled_graph.vs.find(name=i['name'])
                    self.sampled_graph.add_edge(neighbor_id, node_id)
                elif i['name'] not in [n['name'] for n in self.queue]:
                    self.queue.append(i)

if __name__ == "__main__":
    fbego_graph = FBEgoGraph('data/egofb.txt')
    fuck_fa = FirstSearchAlgorithm(fbego_graph, 'depth_first')
    print fuck_fa.validate()
#    fuck_ta = TestAlgorithm(fbego_graph)
#    print fuck_ta.validate()
#    fuck_ta.output_submission()


