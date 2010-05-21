from UserDict import UserDict

class TranspositionTable (UserDict):
    def __init__ (self, maxSize):
        UserDict.__init__(self)
        assert maxSize > 0
        self.maxSize = maxSize
        self.krono = []
        self.maxdepth = 0

        self.killer1 = [-1]*20
        self.killer2 = [-1]*20
        self.hashmove = [-1]*20

    def __setitem__ (self, key, item):
        if not key in self:
            if len(self) >= self.maxSize:
                try:
                    del self[self.krono[0]]
                except KeyError:
                    pass # Overwritten
                del self.krono[0]
        self.data[key] = item
        self.krono.append(key)

    def probe (self, hash, depth, alpha, beta):
        if not hash in self:
            return
        move, score, hashf, ply = self[hash]
        if ply < depth:
            return
        if hashf == hashfEXACT:
            return move, score, hashf
        if hashf == hashfALPHA and score <= alpha:
            return move, alpha, hashf
        if hashf == hashfBETA and score >= beta:
            return move, beta, hashf

    def record (self, hash, move, score, hashf, ply):
        self[hash] = (move, score, hashf, ply)

    def add_killer (self, ply, move):
        if self.killer1[ply] == -1:
            self.killer1[ply] = move
        elif move != self.killer1[ply]:
            self.killer2[ply] = move

    def is_killer (self, ply, move):
        if self.killer1[ply] == move:
            return 10
        elif self.killer2[ply] == move:
            return 8
        if ply >= 2:
            if self.killer1[ply-2] == move:
                return 6
            elif  self.killer2[ply-2] == move:
                return 4
        return 0

    def set_hash_move (self, ply, move):
        self.hashmove[ply] = move

    def is_hash_move (self, ply, move):
        return self.hashmove[ply] == move
