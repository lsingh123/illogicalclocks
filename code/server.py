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
import time

app = Flask(__name__)
machine = None

@app.route('/<time>')
def receive(time):
    global machine
    machine.receive_message(time)
    return "hi"

"""
    A class that creates a virtual machine that sends and receives messages to other
    virtual machines on different ports while keeping track of a logical clock.
"""
class VirtualMachine:
    
    """
        Initializes the virtual machine.

        @param int list | None testing: None if the virtual machine is actually being run. Otherwise, holds
            a list that determines the behavior of the machine. The first number is the
            frequency of the machine. The other numbers determine the bahvior at each step.
            If the number is 0, then the next number in the array will specify the logical
            time that the machine receives at that point in excution. Otherwise, the number
            represents an action from 1 to 10. 1 sends a message to one machine. 2 sends a 
            message to the other machine, 3 sends a message to both, and 4-10 represents
            an internal event. The events in the list are run sequentially.

        @param int id: The id number of the machine
        
        @param int | float speed_multiplier: The multiplier applied to the frequency of the machine. Helpful
            for testing purposes to simulate the machine running for a long time without
            actually running it for that long.
    """
    def __init__(self, testing=None, id=0, speed_multiplier=1):
        self.id = id    # 0, 1, or 2
        self.testing = testing[1:] if testing else None # will hold the array of actions to be served in testing mode
        self.test_index = 0 # index into the testing array
        self.message_queue = queue.Queue()
        self.time = 0 # logical clock time

        # clock tick rate, self.rate events will occur in a single real second
        self.rate = (testing[0] if testing else randrange(1, 7)) * speed_multiplier 

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
            return randrange(1, 11)
        else:
            self.test_index += 1
            try:
                return self.testing[self.test_index - 1]
            except IndexError:
                # When testing and the VM has exhausted all actions, kill the VM (but keep server open)
                sys.exit()

    # Simulates the run of the machine. All logic of how the machine operates is contained here.
    def run_machine(self):
        # Start the server, record the time, define the file name
        self.run_server()
        start_time = time.time()
        filename = f"{self.id}test.txt" if self.testing else f"{self.id}.txt"

        # Remove the file if it exists
        try:
            os.remove(filename)
        except OSError:
            pass

        # Write the first row of the CSV
        with open(filename, "w+") as f:
            writer = csv.writer(f, delimiter = ",")
            writer.writerow(["EVENT", "ID", "TARGET1", "TARGET2", "LOGICAL_TIME", "QUEUE_LENGTH", "TIME", "RATE"])

        while True:
            # sleep for 60/r
            sleep(60/self.rate)

            # In testing mode, simulate receiving messages in the queue if the machine 
            # should receive messages at this part of the deterministic run.
            if self.testing:
                while True:
                    if not self.test_index < len(self.testing):
                        break
                    current_val = self.testing[self.test_index]
                    if current_val != 0:
                        break
                    self.message_queue.put(self.testing[self.test_index + 1])
                    self.test_index += 2

            event = None
            target1, target2 = -1, -1
            message = self.pop_message()
            if message:
                # If a message was in the queue, update the logical clock time
                # appropriately.
                time_received = int(message)
                self.time = max(self.time, time_received) + 1
                event = "received"
            else:
                # If no message was in the queue, randomly select an action
                action = self.get_action()
                self.time += 1

                # Send message to one other machine
                if action in {1, 2}:
                    recipient = self.others[action - 1]
                    self.send_message(recipient)
                    event = "send"
                    target1 = recipient

                # Send messages to both machines
                elif action == 3:    # control group
                # elif action > 2 and action < 6:    # trials 6-7
                # elif action > 2 and action < 8:    # trials 8-9
                    recipient1 = self.others[0]
                    recipient2 = self.others[1]
                    self.send_message(recipient1)
                    self.send_message(recipient2)
                    event = "multisend"
                    target1 = recipient1
                    target2 = recipient2
                else:
                    event = "internal"

            # Log the event and the queue size.
            q_length = self.message_queue.qsize()
            with open(filename, "a+") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([event, self.id, target1, target2, self.time, q_length, int(time.time()-start_time), self.rate])

                
import sys
if __name__ == '__main__':
    # Add command line argument for machine ID, testing mode, and speed multiplier.
    # (See VM documentation on the __init__ method for more details.)
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", help="Machine Id", type=int, default=0)
    parser.add_argument("-t", help=("Optional testing flag. If specified, takes in a file where the first row is a "
                                    "list of ints where the first int is the clock rate, and the next ints are the "
                                    "actions"), default=None)
    parser.add_argument("-s", help="Clock speed multiplier", type=int, default=1)
    
    args = parser.parse_args()

    testargs = None
    if args.t:
        try:
            f = open(args.t)
        except IOError:
            print("Unable to open testing file")
            sys.exit()
        # The testing array, if used, will be on the first line of the specified testing file.
        testargs = [int(i) for i in f.readline().split(" ")]
        f.close()


    # Make sure testing input is valid.
    if testargs:
        # All clock speeds must be between 1 and 6, actions must be >= to 0
        assert 1 <= testargs[0] <= 6, "Invalid clock speed"
        assert all([i >= 0 for i in testargs[1:]]), "Invalid action"
    
    # ID must be 0, 1, or 2, and speed multiplier must be positive
    assert args.s > 0, "Speed multiplier cannot be negative"
    assert 0 <= args.id <= 2, "Id must be in [0, 2]"

    machine = VirtualMachine(id=args.id, testing=testargs, speed_multiplier=args.s)
    machine.run_machine()



