import matplotlib.pyplot as plt
import csv

'''
The code in this file draws space-time diagrams using 0.txt, 1.txt, and 2.txt as input sources.
'''

class Message:

    '''
    This class stores information about each message to be used in graph plotting.
  
    @param: int receiver
        unique ID of the target VM for this message

    @param: int sender
        unique ID of the sending VM for this message

    @param: int time_sent
        time in either logical time ticks or real seconds of the message send.

    @param: int time_received
        time in either logical ticks or real seconds of the message receipt.
        defaults to -1.
        
    '''

    def __init__(self, receiver, sender, time_sent, time_received=-1):
        self.sender = int(sender)
        self.receiver = int(receiver)
        self.send_time = int(time_sent)
        self.receive_time = int(time_received)

'''
load_data: int time_type -> Message list messages, int latest
    loads event information for message send and receipt from all three VM log files and returns 
    list of message events and the latest time of any event.

    @param: string time_type
        the column name corresponding to the type of time being used for this data load. should be 
        either "LOGICAL_TIME" or "TIME" (for system time)
'''
def load_data(time_type):
    messages = []
    latest = 0
    
    # process only sends at first to populate the message list
    for i in range(3):

        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")

            # populate headers to make future row indexes easier
            headers = {}
            row = next(reader)
            for k in range(len(row)):
                headers.update({row[k]:k})

            # iterate over rows in file, focusing on sends and multisends 
            for row in reader:
                if (row[headers["EVENT"]] == "send"):
                    messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers[time_type]]))
                if (row[headers["EVENT"]] == "multisend"):
                    messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers[time_type]]))         
                    messages.append(Message(row[headers["TARGET2"]], row[headers["ID"]], row[headers[time_type]]))

    # we want to process sends in order of receipt 
    # FIFO queue message processing means that a receipt will correspond to the earliest unclaimed message
    messages.sort(key= lambda m: m.send_time)

    # process receive events 
    for i in range(3):
        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")

            # skip headers
            next(reader)

            for row in reader:
                if (row[headers["EVENT"]] == "received"):

                    # grab the next message that is intended for this target and hasn't been received yet
                    # this works because the messages list is sorted by send time and messages are processed FIFO
                    message = None
                    for m in messages:
                        if int(m.receiver) == i and int(m.receive_time) == -1:
                            message = m
                            break
                    message.receive_time = int(row[headers[time_type]])

    latest = max([max(messages, key=lambda m: m.receive_time).receive_time, max(messages, key=lambda m: m.send_time).send_time])

    return messages, latest

'''
make_figure: string time_type, string time_label -> None
    draws the space time diagram

    @param string time_type
        same as time_type parameter for load_data function

    @param: time_label
        label to be displayed on the x-axis
'''
def make_figure(time_type, time_label):
    messages, latest = load_data(time_type)

    # giving ourselves some wiggle room
    latest += 2

    # basic plot setup
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0,latest)
    ax.set_ylim(0,10)
    ax.get_yaxis().set_visible(False)

    xmin = 0
    xmax = latest
    y = 0
    height = 1

    # add lines correpsonding to each VM
    for i in range(3):
        y = y + 2.5
        plt.text(xmin - 0.1*(xmax-xmin), y, f"VM {i}")
        plt.hlines(y , xmin, xmax, label=f"VM {i}")
        plt.vlines(xmin, y - height / 2., y + height / 2.)
        plt.vlines(xmax, y - height / 2., y + height / 2.)

    # add sends, receives, and connection arrows
    for message in messages:
        plt.plot(message.send_time, (message.sender+1)*2.5, 'ro', ms=5, mfc='r')

        # no arrow or receipt for messages that were never received
        if message.receive_time > -1:
            plt.plot(message.receive_time, (message.receiver + 1) *2.5, 'bo', ms=5, mfc='b')

            # draw the arrow
            dx = message.receive_time - message.send_time
            dy = (message.receiver+ 1) *2.5 - (message.sender+1)*2.5
            plt.arrow(message.send_time, (message.sender+1)*2.5, dx, dy, head_length=(xmax-xmin)*0.01, head_width = 0.2, length_includes_head=True)

    plt.xlabel(time_label)
    plt.title("Space Time Diagram for Message Sends and Receives")

    plt.show()

if __name__ == '__main__':
    make_figure("LOGICAL_TIME", "Logical Time")
    make_figure("TIME", "Seconds Elapsed")
