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

def is_maximize():
    return GENETIC_ALGORITHM.getMinimax == Consts.minimaxType['maximize']

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
    mm = GP_MAX if is_maximize() else GP_MIN
    if mm == GP_MAX:
        assert(player == BLACK)
        l = len(model.legal_moves())
    if mm == GP_MIN:
        model.curr_state.to_move = WHITE
        l = len(model.legal_moves())
        model.curr_state.to_move = player
    return l


def gp_num_isolated_pieces(model):
    return 0


def gp_opposition(model):
    mm = GP_MAX if is_maximize() else GP_MIN
    if mm == GP_MAX:
        return model.curr_state.has_opposition(BLACK)
    else:
        return model.curr_state.has_opposition(WHITE)


terminals = [
        "gp_opposition",
        "gp_num_legal_moves",
        "gp_num_isolated_pieces",
        "gp_num_of_captures",
        ]
#===============================================================================
#  -- Non-terminal funcs
#===============================================================================

def ngp_sum(f1, f2):
    def sum_func(model):
        return f1(model) + f2(model)
    return sum_func

def ngp_reverse(f):
    def reverse_func(model):
        return -f(model)
    return reverse_func
