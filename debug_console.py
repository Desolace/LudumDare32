from __future__ import print_function
from threading import Thread
import sys
import re
import curses
#import readline
import pygame
import input_manager as input

if sys.version_info[0] == 3:
    from queue import Queue
else:
    from Queue import Queue

"""
The debug console reads from standard input.
It accepts any expression.
The print statement is mapped to the print() function for printing.
The game state is mapped to a 'game' variable.
Since only expressions are accepted, use setattr to assign values to the game state.
Note that this could be a security hole in production, builtins are allowed, and so the __import__ function is available.

Functions as a wrapper around a Game object, passing control to the game object when needed.
"""
class DebugConsole(object):
    def __init__(self, state):
        self._command_queue = Queue()
        self._response_queue = Queue()
        self._response_queue.put("Debug console enabled.")

        self._state = state
        self._input_thread = Thread(target=self._run_input_thread)
        self._input_thread.daemon = True
        self._input_thread.start()

    def _input_loop(self, screen):

      if sys.version_info[0] < 3:
          input = raw_input

      while True:
          output = self._response_queue.get()
          if output is not None:
              print(output)
          #command = input(">> ")
          #self._command_queue.put(command)

    def _run_input_thread(self):
        self._input_loop(None)

    def parse_commands(self):
        while not self._command_queue.empty():
            try:
                output = eval(self._command_queue.get(),
                                {},
                                {
                                    'pygame':pygame,
                                    'game':self._state
                                })
                self._response_queue.put(output)
            except Exception as e:
                self._response_queue.put(e)

    @property
    def is_running(self):
        return self._state.is_running

    def run_loop(self):
        if self._state.is_running:

            self._state.run_loop()
            self.parse_commands()
        else:
            self._input_thread.join(2)
