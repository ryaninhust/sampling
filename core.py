from validate import validate_sampling

class AlgorithmNoResultError(Exception):
    pass


class Algorithm(object):
    seed_graph = None
    validate_graph = None

    def __init__(self, validate_graph):
        self.validate_graph = validate_graph

    def run(self):
        raise NotImplementedError

    def _validate(self):
        close_validate, kl = validate_sampling(self.graph, self.validate_graph)
        return close_validate, kl

    def validate(self):
        self.seed_graph = self.run()
        if not self.seed_graph:
            raise AlgorithmNoResultError
        close_validate, kl = self._validate
        return close_validate, kl

