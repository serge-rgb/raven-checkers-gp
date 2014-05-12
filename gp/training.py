from gamemanager import GameManager
from gp.criteria import *

from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Selectors

import pyevolve

error_accum = Util.ErrorAccumulator()
NUM_MATCHES = 3.0



class TrainingContext():
    def __init__(self, fitness_func):
        class ThinkTime:
            def get(self):
                return 0.01
        self.thinkTime = ThinkTime()
        self.manager = GameManager(root=None, parent=self, training=True, fitness = fitness_func)

def eval_func(chromosome):
    global error_accum
    error_accum.reset()
    code_comp = chromosome.getCompiledCode()
    fitness_func = eval(code_comp)
    avg_score = 0
    for i in xrange(int(NUM_MATCHES)):
        ctx = TrainingContext(fitness_func)
        avg_score += 8 - len(ctx.manager.model.curr_state.get_pieces(WHITE))
    avg_score /= NUM_MATCHES
    error_accum += (8, avg_score) # target
    return error_accum.getRMSE()


def train():
    import sys
    sys.setrecursionlimit(15000)
    'Play a match between a GPController and a alpha beta controller'
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=5, method="ramped")
    genome.evaluator +=  eval_func

    ga = GSimpleGA.GSimpleGA(genome)
    # This method will catch and use every function that
    # begins with "gp", but you can also add them manually.
    # The terminals are Python variables, you can use the
    # ephemeral random consts too, using ephemeral:random.randint(0,2)
    # for example.

    ga.setParams(gp_terminals      = terminals,
                gp_function_prefix = "ngp")

    # You can even use a function call as terminal, like "func()"
    # and Pyevolve will use the result of the call as terminal
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(20)
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.08)
    ga.setPopulationSize(20)
    # ga.setMultiProcessing()
    set_ga(ga)
    ga(freq_stats=1)

    f = open('fitness_func.txt', 'w')
    with f:
        f.write(str(ga.bestIndividual()).split("Expression: ")[1])
    print ga.bestIndividual()
    print '=========== python code written to fitness_func.txt'


if __name__ == '__main__':
    train()

