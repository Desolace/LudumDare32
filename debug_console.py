from __future__ import print_function
from threading import Thread
import sys
import re
import readline

import pygame
import input_manager as input

if sys.version_info[0] == 3:
    from queue import Queue
else:
    from Queue import Queue

class DebugConsole(object):
    def __init__(self, state):
        self._command_queue = Queue()
        self._response_queue = Queue()
        self._response_queue.put(None)

        self._state = state
        self._input_thread = Thread(target=self._run_input_thread)
        self._input_thread.daemon = True
        self._input_thread.start()

    def _run_input_thread(self):
        if sys.version_info[0] < 3:
            input = raw_input

        while True:
            output = self._response_queue.get()
            if output is not None:
                print(output)
            command = input()
            self._command_queue.put(command)

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
        self._state.run_loop()
        self.parse_commands()
