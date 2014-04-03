from globalconst import *
#===============================================================================
#  -- Terminal funcs
#===============================================================================

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
    pcs = model.curr_state.get_pieces(BLACK)
    return len(model.legal_moves())


def gp_num_isolated_pieces(model):
    return 0


def gp_opposition(model):
    return model.curr_state.has_opposition(BLACK)


#===============================================================================
#  -- Non-terminal funcs
#===============================================================================

