#!usr/bin/env python3

from flask import Flask
import threading
import queue
import requests
from random import randrange
from time import sleep
import argparse

app = Flask(__name__)
machine = None

@app.route('/<time>')
def receive(time):
    global machine
    machine.receive_message(time)
    return "hi"

class VirtualMachine:
    
    def __init__(self, testing=None, id=0):
        self.id = id    # 0, 1, or 2
        self.testing = testing # will hold the array of actions to be served in testing mode
        self.test_index = 0 # index into the testing array
        self.message_queue = queue.Queue()
        self.time = 0 # logical clock time
        self.rate = randrange(1, 6) # clock tick rate, self.rate events will occur in a single real second

        # ID's of the other virtual machines this machine will talk to
        self.others = [0, 1, 2]
        self.others.remove(self.id) 
             
    # put a message in the message queue
    # a message just contains the logical clock time
    def receive_message(self, time):
        if not self.testing:
            self.message_queue.put(time)
 
    # return a message from the message queue, or None if queue is empty
    def pop_message(self):
        if self.message_queue.empty():
            return None

        # might make more sense to put all the logical clock stuff in the logging/file writing functions
        self.time += 1
        if not self.testing:
            return self.message_queue.get()
        else:
            self.test_index += 1
            return self.testing[self.test_index-1]

    # send a message to the target_id containing this machine's logical clock time
    def send_message(self, target_id):
        print(f"sending time {self.time}")
        if not self.testing:
            requests.get(f"http://localhost:500{target_id}/{self.time}")
        self.time += 1

    # start the server in a separate thread to handle multiple connections
    def run_server(self):
        if not self.testing:
            threading.Thread(target=app.run, kwargs={"debug":False, "host":"localhost", "port":5000+self.id}).start()
    
    # get the next action that this machine should perform 
    def get_action(self):
        if not self.testing:
            return randrange(1, 10)
        else:
            self.test_index += 1
            return self.testing[self.test_index - 1]

    def run_machine(self):
        self.run_server()
        
        while True:
            print(f"hi {self.id} {self.time}")
            # sleep for 60/rate seconds 
            sleep(60/self.rate)

            action = self.get_action()

            message = self.pop_message()
            if message:
                print(f"got message {message}")

            # idk what the diff is between 1 and 2 the specs are vague
            elif action == 1 or action == 2:
                self.send_message(self.others[0])

            elif action == 3:
                self.send_message(self.others[0])
                self.send_message(self.others[1])

            else:
                self.time += 1
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", help="Machine Id", default='0')
    args = parser.parse_args()

    machine = VirtualMachine(id=int(args.id))
    machine.run_machine()



