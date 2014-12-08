from algorithms import FirstSearchAlgorithm, BruteAlgorithm
from random_jump import RandomJump
from snow_ball import SnowBallSampling
from forest_fire import ForestFire
from random_walk import RandomWalk
from albatross_sampling import AlbatrossSampling
from frontier_sampling import MDRandomWalk
from metropolis_hastings_random_walk import MHRandomWalk
from multiple_independent_random_walk import MIRandomWalk

from egraphs import FBEgoGraph, RemoteGraph

fb_graph = RemoteGraph('data/public.txt')

fuck_fsa_random = FirstSearchAlgorithm(fb_graph, 'random_first')
fuck_fsa_breadth = FirstSearchAlgorithm(fb_graph, 'breadth_first')
fuck_fsa_width = FirstSearchAlgorithm(fb_graph, 'depth_first')
fuck_sbs = SnowBallSampling(fb_graph)
fuck_ff = ForestFire(fb_graph)
fuck_rj = RandomJump(fb_graph)
fuck_ta = BruteAlgorithm(fb_graph)
fuck_rw = RandomWalk(fb_graph)
fuck_abs = AlbatrossSampling(fb_graph)
fuck_md = MDRandomWalk(fb_graph)
fuck_mhr = MHRandomWalk(fb_graph)
fuck_mir = MIRandomWalk(fb_graph)

a = [fuck_rj, fuck_ff, fuck_sbs, fuck_fsa_width, fuck_fsa_random, fuck_fsa_breadth,
     fuck_ta, fuck_rw, fuck_abs, fuck_md, fuck_mhr, fuck_mir]

for method in a[:]:
    print method.__class__.__name__, method.validate()
    print method.sampled_graph.summary()
