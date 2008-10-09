import sys
import games
from globalconst import *

class Player(object):
    def __init__(self, color):
        self.col = color

    def _get_color(self):
        return self.col
    color = property(_get_color, doc="Player color")

class AlphabetaPlayer(Player):
    def __init__(self, color, depth=4):
        Player.__init__(self, color)
        self.searchDepth = depth

    def select_move(self, game, state):
        sys.stdout.write('\nThinking ... ')
        movelist = games.alphabeta_search(state, game, False,
                                          self.searchDepth)
        positions = []
        step = 2 if game.captures_available(state) else 1
        for i in range(0, len(movelist), step):
            idx, old, new = movelist[i]
            positions.append(str(CBMAP[idx]))
        move = '-'.join(positions)
        print 'I move %s' % move
        return movelist

class HumanPlayer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def select_move(self, game, state):
        while 1:
            moves = game.legal_moves(state)
            positions = []
            idx = 0
            while 1:
                reqstr = 'Move to? ' if positions else 'Move from? '
                # do any positions match the input
                pos = self._valid_pos(raw_input(reqstr), moves, idx)
                if pos:
                    positions.append(pos)
                    # reduce moves to number matching the positions entered
                    moves = self._filter_moves(pos, moves, idx)
                    if game.captures_available(state):
                        idx += 2
                    else:
                        idx += 1
                    if len(moves) <= 1:
                        break
            if len(moves) == 1:
                return moves[0]
            else:
                print "Illegal move!"

    def _valid_pos(self, pos, moves, idx):
        t_pos = IMAP.get(pos.lower(), 0)
        if t_pos == 0:
            return None  # move is illegal
        for m in moves:
            if idx < len(m) and m[idx][0] == t_pos:
                return t_pos
        return None

    def _filter_moves(self, pos, moves, idx):
        del_list = []
        for i, m in enumerate(moves):
            if pos != m[idx][0]:
                del_list.append(i)
        for i in reversed(del_list):
            del moves[i]
        return moves
