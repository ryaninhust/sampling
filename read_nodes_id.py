import sys
import networkx as nx
import random

sys.path.append('/home/peachran/Desktop/hw3/HW3')

def read_graph():
	G = nx.Graph()
	with open('public_nodes.txt','r') as f:
		f.readline()
		for data in f:
			G.add_node(data.strip().split()[0])
	with open('public_edges.txt','r') as f:
		#f.readline()
		#f.readline()
		for data in f:
			G.add_edge(data.strip().split(',')[0],data.strip().split(',')[1])
	return G

def search_by_id(G,node_id):
	graph_array = []
	f = open('node_node.txt','w')
	f.write('\n' + '\n' + node_id +' '+ str(nx.degree(G,node_id))+'\n')
	neigh =  nx.neighbors(G,node_id)
	for i in neigh:
		graph_array.append((i,nx.degree(G,i)))
		f.write(i + ' ' + str(nx.degree(G,i))+'\n')
	f.close()
def main():
	G = read_graph()
	search_by_id(G,'2014')

if __name__ == '__main__':
	main()