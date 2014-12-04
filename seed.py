import random

from igraph import Graph


def generate_seed_graph(origin_graph, k):
    g = Graph.Read_Ncol(origin_graph, directed=False)
    g = g.simplify()

    degree_dict = {}
    vcounts = g.vcount()
    init_seed = random.randint(0, vcounts)

    seed_graph = Graph()
    seed_graph.add_vertex(init_seed)
    degree_dict[init_seed] = g.neighborhood_size(init_seed) - 1

    while seed_graph.vcount() != k:
        choiced_vertex = random.choice(seed_graph.vs)
        choiced_neighor = random.choice(g.neighbors(choiced_vertex['name']))
        if str(choiced_neighor) in seed_graph.vs['name']:
            continue
        seed_graph.add_vertex(choiced_neighor)
        degree_dict[choiced_neighor] = g.neighborhood_size(choiced_neighor) - 1
        choiced_neighor_neighor = g.neighbors(choiced_neighor)
        #choiced_neighor_neighor = [str(i) for i in choiced_neighor_neighor]
        existed_nodes = set(choiced_neighor_neighor) & set(seed_graph.vs['name'])


        for node in existed_nodes:
            choiced_neighor_id = filter(lambda x: x['name'] == choiced_neighor, seed_graph.vs)[0].index
            node_id = filter(lambda x: x['name'] == node, seed_graph.vs)[0].index
            seed_graph.add_edge(choiced_neighor_id, node_id)

    return seed_graph, degree_dict

if __name__ == "__main__":
    seed_graph, degrees = generate_seed_graph('data/egofb.txt', 2)
    print seed_graph.vs['name']
    print seed_graph.get_edgelist()
    print degrees
