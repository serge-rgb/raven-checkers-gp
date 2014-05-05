from Tkinter import Widget
from controller import Controller
from globalconst import *
from gp.trainingcanvas import TrainingCanvas
from gp.criteria import *
import copy


# ASSUMPTION: GPController is black.
def get_fitness_func():
    f = open("fitness_func.txt")
    func = None
    with f:
        txt = f.readline()
        print ".... Using fitness func: ", txt
        func = eval(txt)
    return func


class GPController(Controller):
    def __init__(self, **props):
        self._model = props['model']
        self._view = props['view']
        self._fitness = props['fitness']
        self._before_turn_event = None
        self._end_turn_event = props['end_turn_event']
        self._highlights = []
        self._move_in_progress = False
        self._count_turns = 0
        if not self._fitness:
            self._fitness = get_fitness_func()

    def _register_event_handlers(self):
        pass

    def _unregister_event_handlers(self):
        if not isinstance(self._view.canvas, TrainingCanvas):
            Widget.unbind(self._view.canvas, '<Button-1>')

    def stop_process(self):
        pass

    def set_search_time(self, time):
        pass

    def get_player_type(self):
        return HUMAN

    def set_before_turn_event(self, evt):
        self._before_turn_event = evt

    def add_highlights(self):
        for h in self._highlights:
            self._view.highlight_square(h, OUTLINE_COLOR)

    def remove_highlights(self):
        for h in self._highlights:
            self._view.highlight_square(h, DARK_SQUARES)

    def start_turn(self):
        self._register_event_handlers()
        self._model.curr_state.attach(self._view)

        if self._model.terminal_test() or self._count_turns > 50:
            self._before_turn_event()
            self._model.curr_state.attach(self._view)
            # print self._model.curr_state
            return
        moves = self._model.legal_moves()
        self.moves = moves
        if len(moves) > 0:
            self._make_move()
        self._view.canvas.after(0, self._end_turn_event())

    def end_turn(self):
        self._unregister_event_handlers()
        self._model.curr_state.detach(self._view)

    def _filter_moves(self, pos, moves, idx):
        del_list = []
        for i, m in enumerate(moves):
            if pos != m.affected_squares[idx][0]:
                del_list.append(i)
        for i in reversed(del_list):
            del moves[i]
        return moves

    def _make_move(self):
        self._count_turns += 1
        moves = copy.deepcopy(self.moves)
        move = moves[0]
        fitness = 0
        for i in xrange(len(moves)):
            self._model.make_move(self.moves[i])
            f = self._fitness(self._model)
            if fitness < f:
                fitness = f
                move = moves[i]
            self._model.undo_move()

        self._model.make_move(move)
        # a new move obliterates any more redo's along a branch of the game tree
        self._model.curr_state.delete_redo_list()
        self._move_in_progress = False
