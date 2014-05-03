from gamemanager import GameManager
from gp.criteria import *

from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Selectors

import pyevolve

error_accum = Util.ErrorAccumulator()

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
    print 'func: ', fitness_func
    ctx = TrainingContext(fitness_func)
    #
    # Do a series of games HERE =========
    #
    error_accum += (8, 0) # target
    print 'error so far: ', error_accum.getRMSE()
    return error_accum.getRMSE()


def train():
    'Play a match between a GPController and a alpha beta controller'
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=5, method="ramped")
    genome.evaluator +=  eval_func

    ga = GSimpleGA.GSimpleGA(genome)
    set_ga(ga)
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
    ga.setPopulationSize(3)
    ga(freq_stats=5)

    set_ga(ga)

    print ga.bestIndividual()


if __name__ == '__main__':
    train()

