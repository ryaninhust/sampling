from read_nodes_id import *
import numpy as np
import random

def random_walk(G,node,times):
	sub_G = nx.Graph()
	i = 0
	sub_G.add_node(node)
	while i < times:
		neighbors = nx.neighbors(G,node)
		for s in neighbors:
			sub_G.add_edge(node,s)
		new_node =  random.choice(neighbors)
		node = new_node
		i += 1
	return sub_G

def metropolis_hastings_random_walk(G,node):
	sub_G = nx.Graph()
	times = 100
	i = 0
	sub_G.add_node(node)
	while i < times:
		neighbors = nx.neighbors(G,node)
		for s in neighbors:
			sub_G.add_edge(node,s)
		new_node =  random.choice(neighbors)
		if random.random() <= float(G.degree(node))/G.degree(new_node):
			node = new_node
		i += 1
	return sub_G

def multiple_independent_random_walk(G):
	sub_G = nx.Graph()
	times = 10
	i = 0
	node_set = random.sample(G.nodes(),10)
	for s in node_set:
		graph_sub = random_walk(G,s,times)
		sub_G.add_edges_from(graph_sub.edges(data=True))
	return sub_G

def random_jump(G,node):
	sub_G = nx.Graph()
	times = 100
	i = 0
	c = 0.15
	sub_G.add_node(node)
	while i < times:
		alpha = np.random.uniform(0,1)
		if alpha < c:
			new_node = random.choice(G.nodes()) # choose a new random vertex
			sub_G.add_node(new_node)	# add node to sub_G
			sub_G.add_edge(node,new_node)
			node = new_node
		else:
			neighbors = nx.neighbors(G,node)
			for s in neighbors:
				sub_G.add_edge(node,s)
			new_node =  random.choice(neighbors)
			node = new_node		
		i += 1
	return sub_G

def albatross_sampling(G,node):
	sub_G = nx.Graph()
	times = 100
	i = 0
	p = 0.02 # probality of jump
	while i < times:
		alpha = np.random.uniform(0,1)
		if alpha < p:
			new_node = str(np.random.randint(0, G.number_of_nodes())) # choose a new random vertex
			sub_G.add_node(new_node)	# add node to sub_G
			sub_G.add_edge(node,new_node)
			node = new_node
		else:
			neighbors = nx.neighbors(G,node)
			for s in neighbors:
				sub_G.add_edge(node,s)
			new_node =  random.choice(neighbors)
			if random.random() <= float(G.degree(node))/G.degree(new_node):
				node = new_node
		i += 1
	return sub_G

def uniform_independent_sample(G):
	sub_G = nx.Graph()
	times = 100
	i = 0
	while i < times:
		node = random.choice(G.nodes())
		if node in G:
			neighbors = nx.neighbors(G,node)
			for s in neighbors:
				sub_G.add_edge(node,s)
		i += 1
	return sub_G

def frontier_sampling(G): # Also called multi-dimensional random walk(MDRW)
	i = 0
	m = 10
	sub_G = nx.Graph()
	times = 100
	degree_sum = 0
	node_set = random.sample(G.nodes(),10)
	for sv in node_set:
		degree_sum += G.degree(str(sv))
	while i < times:
		alpha = np.random.uniform(0,1)
		for j in xrange(len(node_set)):
			if j == len(node_set)- 1:
				node = node_set[-1]
				break
			else:
				if alpha >= G.degree(str(node_set[j]))/degree_sum and alpha < G.degree(str(node_set[j+1]))/degree_sum:
					node = node_set[j]
					break
		neighbors = G.neighbors(node)
		for s in neighbors:
				sub_G.add_edge(node,s)
		new_node =  random.choice(neighbors)
		node_set[j] = new_node
		i += 1
	return sub_G


class Gene_Graph():
	__instance = None
	@classmethod
	def get_graph(cls):
		if cls.__instance == None:
			cls.__instance = read_graph()
		return cls.__instance

def main():
	G = Gene_Graph.get_graph()
	node = '1'
	# search_by_id(G,'2014')
	# 1.random walk
	'''sub_G = random_walk(G,node,100)	
	print sub_G.nodes(),sub_G.edges()
	# 2.metropolis_hastings_random_walk'''
	'''sub_G = metropolis_hastings_random_walk(G,node)
	print sub_G.nodes(),sub_G.edges()'''
	# 3.albatross_sampling
	'''sub_G = albatross_sampling(G,node)
	print sub_G.nodes(),sub_G.edges()
	# 4.uniform_independent_sampling RNN
	sub_G = uniform_independent_sample(G) 
	print sub_G.nodes(),sub_G.edges()'''
	# 5.random jump RWE
	'''sub_G = random_jump(G,node)
	print sub_G.nodes(),sub_G.edges()'''
	# 6.frontier sampling/MDRW
	'''sub_G = frontier_sampling(G)
	print sub_G.nodes(),sub_G.edges()
	# 7. multiple independent random walk
	sub_G = multiple_independent_random_walk(G)
	print sub_G.nodes(),sub_G.edges()'''

if __name__ == '__main__':
	main()