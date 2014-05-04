from globalconst import *

from pyevolve import Consts

#===============================================================================
#  -- Terminal funcs
#       model: Checkerboard
#       mm: min or max?
#===============================================================================


GENETIC_ALGORITHM = None  # Instance of

def set_ga(ga):
    global GENETIC_ALGORITHM
    GENETIC_ALGORITHM = ga

def gp_num_of_captures(model):
    '0 if no captures...'
    captures = model.captures_available()
    if len(captures) > 0:
        length = -1
        selected = None
        for move in captures:
            l = len(move.affected_squares)
            if l > length:
                length = l
                selected = move
        return len(selected.affected_squares)
    return 0


def gp_num_legal_moves(model):
    'num of squares to which we can move'
    player = model.curr_state.to_move
    l = 0
    assert(player == WHITE)
    l = len(model.legal_moves())
    return l


def _gp_num_isolated_pieces(model):
    return 0


def gp_opposition(model):
    return model.curr_state.has_opposition(BLACK)


terminals = [
        "gp_opposition",
        "gp_num_legal_moves",
        #"gp_num_isolated_pieces",
        "gp_num_of_captures",
        ]
#===============================================================================
#  -- Non-terminal funcs
#===============================================================================

def ngp_sum(f1, f2):
    def sum_func(model):
        return f1(model) + f2(model)
    return sum_func

def _ngp_reverse(f):
    def reverse_func(model):
        return -f(model)
    return reverse_func
