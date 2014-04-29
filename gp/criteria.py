from globalconst import *
#===============================================================================
#  -- Terminal funcs
#       model: Checkerboard
#       mm: min or max?
#===============================================================================


def gp_num_of_captures(model, mm):
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


def gp_num_legal_moves(model, mm):
    'num of squares to which we can move'
    player = model.curr_state.to_move
    l = 0
    if mm == GP_MAX:
        assert(player == BLACK)
        l = len(model.legal_moves())
    if mm == GP_MIN:
        model.curr_state.to_move = WHITE
        l = len(model.legal_moves())
        model.curr_state.to_move = player
    return l


def gp_num_isolated_pieces(model, mm):
    return 0


def gp_opposition(model, mm):
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

def ngp_sum2(f1, f2):
    def func(model, mm):
        return f1(model, mm) + f2(model, mm)

def ngp_reverse(f):
    def func(model, mm):
        return -f(model, mm)
