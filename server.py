#!usr/bin/env python3

from flask import Flask
import threading
import queue
import requests
from random import randrange
from time import sleep
import argparse
import os
import datetime
import csv

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
        self.rate = randrange(1, 7) #* 10 # clock tick rate, self.rate events will occur in a single real second

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
        if self.testing:
            self.test_index += 1
            return self.testing[self.test_index-1]
        else:
            try:
                return self.message_queue.get_nowait()
            except queue.Empty:
                return None
        

    # send a message to the target_id containing this machine's logical clock time
    def send_message(self, target_id):
        if not self.testing:
            requests.get(f"http://localhost:500{target_id}/{self.time}")

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
        filename = f"{self.id}.txt"
        try:
            os.remove(filename)
        except OSError:
            pass

        with open(filename, "w+") as f:
            writer = csv.writer(f, delimiter = ",")
            writer.writerow(["EVENT", "ID", "TARGET1", "TARGET2", "LOGICAL_TIME", "QUEUE_LENGTH", "TIME"])

        while True:
                
            # sleep for 60/r
            sleep(60/self.rate)

            action = self.get_action()

            event = None
            target1, target2 = -1, -1
            message = self.pop_message()
            if message:
                time_received = int(message)
                self.time = max(self.time, time_received) + 1
                event = "received"

            else:

                self.time += 1
                if action in {1, 2}:
                    recipient = self.others[action - 1]
                    self.send_message(recipient)
                    event = "send"
                    target1 = recipient

                elif action == 3:
                    recipient1 = self.others[0]
                    recipient2 = self.others[1]
                    self.send_message(recipient1)
                    self.send_message(recipient2)
                    event = "multisend"
                    target1 = recipient1
                    target2 = recipient2
                else:
                    event = "internal"

            q_length = self.message_queue.qsize()
            with open(filename, "a+") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([event, self.id, target1, target2, self.time, q_length, datetime.datetime.now().time()])
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", help="Machine Id", default='0')
    args = parser.parse_args()

    machine = VirtualMachine(id=int(args.id))
    machine.run_machine()



