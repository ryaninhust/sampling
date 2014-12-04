from collections import Counter

from igraph import Graph
from pymongo import MongoClient
from scipy.stats import entropy

mc = MongoClient()
db = mc.test

GRAPH_PAHT_PARSE = 'data/%s.txt'


def generate_dis(value_list):
    return Counter(value_list)


def merge_dis(counter1, counter2):
    key_list1 = counter1.keys()
    key_list2 = counter2.keys()
    merged_key_list =  set(key_list1) & set(key_list2)
    return merged_key_list


def transform_dis(counter, merged_key_list):
    return [counter[key] for key in merged_key_list]


def valide_dis(origin_dis, test_dis):
    kl = entropy(origin_dis, test_dis)
    return kl


def fetch_degs_list(g):
    degs = []
    for v in g.vs:
        degs.append(v.degree())
    return degs


def fetch_origin_degs_list(collection):
    degs = []
    for node in collection.find():
        degs.append(node['degree'])
    return degs


def valide_degree(g, graph_name):
    collection = db[graph_name]
    origin_counter = generate_dis(fetch_origin_degs_list(collection))
    sampling_counter = generate_dis(fetch_degs_list(g))
    merged_keys = merge_dis(origin_counter, sampling_counter)
    origin_dis_list = transform_dis(origin_counter, merged_keys)
    sampling_dis_list = transform_dis(sampling_counter, merged_keys)
    os = valide_dis(origin_dis_list, sampling_dis_list)
    so = valide_dis(sampling_dis_list, origin_dis_list)
    return 0.5 * (os + so)


def valide_closeness(g, graph_name):
    collection = db[graph_name]
    sampled_graph_closeness_tuple = []
    for v in g.vs[:100]:
        sampled_graph_closeness_tuple.append((v['name'], v.closeness))
    sampled_graph_closeness_tuple.sort(key=lambda x: x[1], reverse=True)

    rank_total = 0
    for node_id, _ in sampled_graph_closeness_tuple:
        global_rank = collection.find_one({'node_id': node_id})['order']
        rank_total += global_rank
    return float(rank_total) / 100


def validate_sampling(sampled_graph, graph_name):
    g = Graph.Read_Ncol(GRAPH_PAHT_PARSE % graph_name, directed=False)
    g.simplify()
    close_validate = valide_closeness(g, graph_name)
    kl = valide_degree(g, graph_name)
    print close_validate, kl
