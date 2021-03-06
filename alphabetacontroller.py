import games
import copy
import multiprocessing
import time
import random
from controller import Controller
from gp.trainingcanvas import TrainingCanvas
from transpositiontable import TranspositionTable
from globalconst import *

class AlphaBetaController(Controller):
    def __init__(self, **props):
        self._model = props['model']
        self._view = props['view']
        self._end_turn_event = props['end_turn_event']
        self._highlights = []
        self._search_time = props['searchtime'] # in seconds
        self._before_turn_event = None
        if not isinstance(self._view.canvas, TrainingCanvas):
            self._parent_conn, self._conn = multiprocessing.Pipe()
            self._term_event = multiprocessing.Event()
        self.process = multiprocessing.Process()
        self._start_time = None
        self._call_id = 0
        self._trans_table = TranspositionTable(50000)

    def set_before_turn_event(self, evt):
        self._before_turn_event = evt

    def add_highlights(self):
        for h in self._highlights:
            self._view.highlight_square(h, OUTLINE_COLOR)

    def remove_highlights(self):
        for h in self._highlights:
            self._view.highlight_square(h, DARK_SQUARES)

    def start_turn(self):
        if self._model.terminal_test():
            self._before_turn_event()
            self._model.curr_state.attach(self._view)
            return
        self._view.update_statusbar('Thinking ...')
        if not isinstance(self._view.canvas, TrainingCanvas):
            self.process = multiprocessing.Process(target=calc_move,
                                                   args=(self._model,
                                                         self._trans_table,
                                                         self._search_time,
                                                         self._term_event,
                                                         self._conn))
        self._start_time = time.time()
        if not isinstance(self._view.canvas, TrainingCanvas):
            self.process.daemon = True
            self.process.start()
        self._view.canvas.after(0, self.get_move)

    def get_move(self):
        #if self._term_event.is_set() and self._model.curr_state.ok_to_move:
        #    self._end_turn_event()
        #    return
        if not isinstance(self._view.canvas, TrainingCanvas):
            self._highlights = []
            moved = self._parent_conn.poll()
            while (not moved and (time.time() - self._start_time)
                   < self._search_time * 2):
                self._call_id = self._view.canvas.after(1, self.get_move)
                return
            if not isinstance(self._view.canvas, TrainingCanvas):
                self._view.canvas.after_cancel(self._call_id)
            move = self._parent_conn.recv()
        # ----------------------------------------------------------------------
        else:  # We actually want to go fast
            move = calc_move(self._model, self._trans_table, self._search_time, None)
            #if self._model.curr_state.ok_to_move:
        self._before_turn_event()

        # highlight remaining board squares used in move
        step = 2 if len(move.affected_squares) > 2 else 1
        for m in move.affected_squares[0::step]:
            idx = m[0]
            self._view.highlight_square(idx, OUTLINE_COLOR)
            self._highlights.append(idx)

        self._model.curr_state.attach(self._view)
        self._model.make_move(move, None, True, True,
                              self._view.get_annotation())
        # a new move obliterates any more redo's along a branch of the game tree
        self._model.curr_state.delete_redo_list()
        self._end_turn_event()

    def set_search_time(self, time):
        self._search_time = time # in seconds

    def stop_process(self):
        self._term_event.set()
        if not isinstance(self._view.canvas, TrainingCanvas):
            self._view.canvas.after_cancel(self._call_id)

    def end_turn(self):
        self._view.update_statusbar()
        self._model.curr_state.detach(self._view)

def longest_of(moves):
    length = -1
    selected = None
    for move in moves:
        l = len(move.affected_squares)
        if l > length:
            length = l
            selected = move
    return selected

def calc_move(model, table, search_time, conn):
    move = None
    # term_event.clear()
    captures = model.captures_available()
    if captures:
        time.sleep(0)
        move = longest_of(captures)
    else:
        depth = 0
        start_time = time.time()
        curr_time = start_time
        checkpoint = start_time
        model_copy = copy.deepcopy(model)
        while 1:
            depth += 1
            table.set_hash_move(depth, -1)
            move = games.alphabeta_search(model_copy.curr_state,
                                          model_copy,
                                          depth)
            checkpoint = curr_time
            curr_time = time.time()
            rem_time = search_time - (curr_time - checkpoint)
            # if term_event.is_set(): # a signal means terminate
            #     term_event.clear()
            #     move = None
            #     break
            if (curr_time - start_time > search_time or
               ((curr_time - checkpoint) * 2) > rem_time or
               depth > MAXDEPTH):
                break
    if conn:
        conn.send(move)
    else:
        return move
    #model.curr_state.ok_to_move = True
