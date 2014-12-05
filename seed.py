import random

from igraph import Graph


def generate_seed_graph(origin_graph, k):
    g = Graph.Read_Ncol(origin_graph, directed=False)
    g = g.simplify()

    vcounts = g.vcount()
    init_seed = random.randint(0, vcounts)

    seed_graph = Graph(directed=False)
    seed_graph.add_vertex(g.vs[init_seed]['name'], degree=g.degree(init_seed))

    while seed_graph.vcount() != k:
        choiced_vertex = random.choice(seed_graph.vs)
        choiced_vertex_index = g.vs.find(name=choiced_vertex['name'])
        choiced_neighor = g.vs[random.choice(g.neighbors(choiced_vertex_index))]
        if choiced_neighor['name'] in seed_graph.vs['name']:
            continue
        seed_graph.add_vertex(choiced_neighor['name'], degree=g.degree(choiced_neighor['name']))
        choiced_neighor_neighor = g.neighbors(choiced_neighor.index)
        choiced_neighor_neighor_name = [g.vs[i]['name'] for i in choiced_neighor_neighor]
        existed_nodes = set(choiced_neighor_neighor_name) & set(seed_graph.vs['name'])


        for node in existed_nodes:
            choiced_neighor_id = seed_graph.vs.find(name=choiced_neighor['name']).index
            node_id = seed_graph.vs.find(name=node).index
            seed_graph.add_edge(choiced_neighor_id, node_id)

    return seed_graph

if __name__ == "__main__":
    seed_graph, degrees = generate_seed_graph('data/egofb.txt', 4)
    print seed_graph.vs[0]
    print seed_graph.get_edgelist()
    print degrees
