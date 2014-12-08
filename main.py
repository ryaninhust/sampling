from algorithms import FirstSearchAlgorithm, BruteAlgorithm
from random_jump import RandomJump
from snow_ball import SnowBallSampling
from forest_fire import ForestFire

from egraphs import FBEgoGraph

fb_graph = FBEgoGraph('data/hepth.txt')

fuck_fsa_random = FirstSearchAlgorithm(fb_graph, 'random_first')
fuck_fsa_breadth = FirstSearchAlgorithm(fb_graph, 'breadth_first')
fuck_fsa_width = FirstSearchAlgorithm(fb_graph, 'depth_first')
fuck_sbs = SnowBallSampling(fb_graph)
fuck_ff = ForestFire(fb_graph)
fuck_rj = RandomJump(fb_graph)
fuck_ta = BruteAlgorithm(fb_graph)

a = [fuck_rj, fuck_ff, fuck_sbs, fuck_fsa_width, fuck_fsa_random, fuck_fsa_breadth,
     fuck_ta]

for method in a:
    print method.validate()
