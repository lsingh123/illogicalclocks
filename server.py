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
        self.id = id
        self.testing = testing
        self.test_index = 0
        self.message_queue = queue.Queue()
        self.time = 0
        self.rate = randrange(1, 6)

        print(self.id)
        self.others = [0, 1, 2]
        self.others.remove(self.id)
             
    def receive_message(self, time):
        if not self.testing:
            self.message_queue.put(time)
 
    def pop_message(self):
        if self.message_queue.empty():
            return None

        # might make more sense to put all the logical stuff in the logging/file writing functions
        # your call Luke whatever makes your life easier
        self.time += 1
        if not self.testing:
            return self.message_queue.get()
        else:
            self.test_index += 1
            return self.testing[self.test_index-1]

    def send_message(self, target_id):
        print(self.time)
        if not self.testing:
            requests.get(f"http://localhost:500{target_id}/{self.time}")
        self.time += 1

    def run_server(self):
        if not self.testing:
            threading.Thread(target=app.run, kwargs={"debug":False, "host":"localhost", "port":5000+self.id}).start()

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
                print(message)

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



