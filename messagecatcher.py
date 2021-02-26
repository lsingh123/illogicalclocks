#!/usr/bin/env python3

import queue

class MessageCatcher:
    '''The MessageCatcher class handles all server-side messaging logic.'''

    def __init__(self, id=0, testing=None):
        self.id = id
        self.testing = testing
        self.test_index = 0
        self.message_queue = queue.Queue()
            
    def add_message(self, time):
        if !self.testing:
            self.message_queue.put(time)

    def get_message(self):
        if !self.testing:
            return self.message_queue.get()
        else:
            self.test_index += 1
            return self.testing[self.test_index-1]
