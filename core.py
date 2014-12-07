import os
from collections import Counter
from validate import validate_sampling

class AlgorithmNoResultError(Exception):
    pass


class Algorithm(object):
    egraph = None
    name = None
    degree_dis = None
    top_k = 100
    top_k_closeness = None

    def __init__(self, egraph):
        self.egraph = egraph
        self.sampled_graph = egraph.seed_graph.copy()
        self.origin_graph = egraph.origin_graph

    def run(self, k, **kwarg):
        raise NotImplementedError

    def _validate(self):
        close_validate, kl = validate_sampling(self)
        return close_validate, kl

    def validate(self, k=100):
        self.run(k)
        #if self.sampled_graph.vcount() == self.egraph.seed_graph.vcount():
        #    raise AlgorithmNoResultError
        self.cal_sample_degree_dist()
        self.cal_clossness_rank()
        close_validate, kl = self._validate()
        return close_validate, kl

    def cal_sample_degree_dist(self):
        sampled_degree = self.sampled_graph.degree()
        self.degree_dis = self.cal_degree_dist(sampled_degree)

    def cal_degree_dist(self, degree):
        degree_counter = Counter(degree)

        degree_bin = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 10), (11, 15),
                      (16, 21), (22, 28), (29, 36), (37, 45), (46, 55),
                      (56, 70), (71, 100), (101, 200), (201,)]

        degree_bin_counter = {}
        for _bin in degree_bin:
            if len(_bin) == 2:
                bin_counter = sum([degree_counter[key]
                                for key in degree_counter.keys()
                                if key in range(_bin[0], _bin[1]+1)])
            else:
                bin_counter = sum([degree_counter[key]
                                for key in degree_counter.keys()
                                if key >= _bin[0]])
            degree_bin_counter[_bin] = bin_counter
        bin_counter_sum = sum(degree_bin_counter.values())
        normalize_bin_counter = {i[0]: float(i[1]) / bin_counter_sum
                                 for i in degree_bin_counter.items()}

        for i in normalize_bin_counter.items():
            if i[1] == 0:
                normalize_bin_counter[i[0]] = 0.000006
        assert sum(normalize_bin_counter.values()) < 1.0001
        return [(key, normalize_bin_counter[key]) for key in degree_bin]

    def cal_clossness_rank(self):
        rank_clossness = []
        for v in self.sampled_graph.vs:
            rank_clossness.append((v['name'], v.closeness()))
        rank_clossness.sort(reverse=True, key=lambda x: x[1])
        self.top_k_closeness = rank_clossness[:self.top_k]
    def output_submission(self):
        path = 'result/%s_%s' % (self.name, self.egraph.name)
        os.mkdir(path)
        with open(path+'/sample.txt', 'w') as sample:
            for i in self.sampled_graph.es:
                sample.write('%s %s\n' % (i.source, i.target))
        with open(path+'/closeness.txt', 'w') as closeness:
            for i in self.top_k_closeness:
                closeness.write('%s\n' % i[0])
        with open(path+'/degree.txt', 'w') as degree:
            for i in self.degree_dis:
                if len(i[0]) == 2:
                    degree.write('%s %s %f\n' % (i[0][0], i[0][1], i[1]))
                else:
                    degree.write('%s %f\n' % (i[0][0], i[1]))



