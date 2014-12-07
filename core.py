from validate import validate_sampling
class AlgorithmNoResultError(Exception):
    pass


class Algorithm(object):
    egraph = None

    def __init__(self, egraph):
        self.egraph = egraph
        self.sampled_graph = egraph.seed_graph.copy()
        self.origin_graph = egraph.origin_graph

    def run(self, k):
        raise NotImplementedError

    def _validate(self):
        close_validate, kl = validate_sampling(self.sampled_graph, self.egraph.name)
        return close_validate, kl

    def validate(self, k=100):
        self.run(k)
        #if self.sampled_graph.vcount() == self.egraph.seed_graph.vcount():
        #    raise AlgorithmNoResultError
        close_validate, kl = self._validate()
        return close_validate, kl

