from requests import get
from igraph import Graph

DOMAIN_PATH = "http://140.112.31.186"
TEAM_SECRET = "h6Qtbh81js"
SEED_URL_PARSE = "{0}/SNA2014/hw3/query_public.php?team={1}"
NODE_URL_PARSE = "{0}/SNA2014/hw3/query_public.php?team={1}&node={2}"

def query_seed():
    data = get(SEED_URL_PARSE.format(DOMAIN_PATH, TEAM_SECRET))
    g = parse_seed_response(data.content)
    return g


def query_single_node(node, node_attribute_count):
    data = get(NODE_URL_PARSE.format(DOMAIN_PATH, TEAM_SECRET, node)).content
    nodes_list = []
    lines = data.splitlines()
    for i in lines[3:]:
        node_dict = parse_neighours(i, node_attribute_count)
        nodes_list.append(node_dict)
    return nodes_list


def parse_seed_response(data):
    g = Graph(directed=False)
    lines = data.splitlines()
    #query_count = lines[1]
    node_attr, edge_attr = [int(i) for i in lines[2].split(' ')]
    node_count = int(lines[3])
    for i in lines[4: node_count+4]:
        attr_dict = parse_node_attribute(i, node_attr)
        if not attr_dict:
            continue
        g.add_vertex(**attr_dict)
    for i in lines[node_count+5:]:
        attr_dict = parse_edge_attribute(i, edge_attr)
        if not attr_dict:
            continue
        g.add_edge(**attr_dict)
    return g, node_attr, edge_attr


def parse_node_attribute(line, node_attr_count):
    splited_attrs = line.strip().split(' ')
    if len(splited_attrs) < 1:
        return
    attr_dict = {}
    name = splited_attrs[0]
    attr_dict['name'] = name
    degree = int(splited_attrs[1])
    attr_dict['degree'] = degree
    for i in range(node_attr_count):
        attr_dict['attr_%d' % i] = splited_attrs[2+i]
    return attr_dict


def parse_edge_attribute(line, edge_attr_count):
    splited_attrs = line.strip().split(' ')
    if len(splited_attrs) < 2:
        return
    attr_dict = {}
    attr_dict['source'] = splited_attrs[0]
    attr_dict['target'] = splited_attrs[1]
    for i in range(edge_attr_count):
        attr_dict['attr_%d' % i] = splited_attrs[2+i]
    return attr_dict


def parse_neighours(line, node_attr_count):
    splited_attrs = line.strip().split(' ')
    node_dict = {}
    if len(splited_attrs) < 1:
        return
    neighour_name = splited_attrs[0]
    node_dict["name"] = neighour_name
    degree = int(splited_attrs[1])
    node_dict['degree'] = degree
    for i in range(node_attr_count):
        node_dict['attr_%d' % i] = splited_attrs[2+i]
    return node_dict


if __name__ == "__main__":
    print query_seed()
