from pymongo import MongoClient
from scipy.stats import entropy

mc = MongoClient()
db = mc.test


def valide_dis(origin_dis, test_dis):
    kl = entropy(origin_dis, test_dis)
    return kl


def fetch_origin_degs_list(collection):
    degs = []
    for node in collection.find():
        degs.append(int(node['degree']))
    return degs


def validate_degree(algorithm):
    collection = db[algorithm.egraph.name]
    origin_degree_dist = algorithm.cal_degree_dist(fetch_origin_degs_list(collection))
    sampled_degree_dist = algorithm.degree_dis
    origin_prob = [i[1] for i in origin_degree_dist]
    sampled_prob = [i[1] for i in sampled_degree_dist]
    os = valide_dis(origin_prob, sampled_prob)
    so = valide_dis(sampled_prob, origin_prob)
    return 0.5 * (os + so)


def validate_closeness(algorithm):
    collection = db[algorithm.egraph.name]
    sampled_graph_closeness_tuple = algorithm.top_k_closeness

    rank_total = 0
    for node_id, _ in sampled_graph_closeness_tuple:
        global_rank = collection.find_one({'node_id': node_id})['order']
        rank_total += global_rank
    return float(rank_total) / algorithm.top_k


def validate_sampling(algorithm):
    close_validate = validate_closeness(algorithm)
    kl = validate_degree(algorithm)
    return close_validate, kl
