import sys
import networkx as nx
import random

def read_graph():
	G = nx.Graph()
	with open('egofb_nodes.txt','r') as f:
		f.readline()
		for data in f:
			G.add_node(data.strip().split()[0])
	with open('egofb_edges.txt','r') as f:
		f.readline()
		f.readline()
		for data in f:
			G.add_edge(data.strip().split(' ')[0],data.strip().split(' ')[1])
	return G

def search_by_id(G,node_id):
	graph_array = []
	#f = open('node_node.txt','w')
	#f.write('\n' + '\n' + node_id +' '+ str(nx.degree(G,node_id))+'\n')
	nodes_list = []
	node_dict = {}
	node_dict['name'] = node_id
	node_dict['degree'] = nx.degree(G,node_id)
	for i in xrange(5):
		node_dict['attr_'+str(i)] = str(0)
	nodes_list.append(node_dict)
	neigh =  nx.neighbors(G,node_id)
	for i in neigh:
		node_dict['name'] = i
		node_dict['degree'] = nx.degree(G,i)
		for i in xrange(5):
			node_dict['attr_'+str(i)] = str(0)
		nodes_list.append(node_dict)
	return nodes_list

class Gene_Graph():
	__instance = None
	@classmethod
	def get_graph(cls):
		if cls.__instance == None:
			cls.__instance = read_graph()
		return cls.__instance

def main():
	G = Gene_Graph.get_graph()
	print search_by_id(G,'1')
if __name__ == '__main__':
	main()