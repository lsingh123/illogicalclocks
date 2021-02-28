import matplotlib.pyplot as plt
import csv


class Message:

    '''
    This class stores information about each message
    '''

    '''
    @param: int receiver. unique ID of the target VM for this message

    @param: int sender. unique ID of the sending VM for this message

    @param: int time_sent. time in either logical time ticks or real seconds of the message send.

    @param: int time_received. time in either logical ticks or real seconds of the message receipt.
    '''

    def __init__(self, receiver, sender, time_sent, time_received=-1):
        self.sender = int(sender)
        self.receiver = int(receiver)
        self.send_time = int(time_sent)
        self.receive_time = int(time_received)

def load_data(time_type):
    messages = []
    latest = 0
    
    # process sends
    headers = {}
    for i in range(3):
        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            headers = {}
            row = next(reader)
            for k in range(len(row)):
                headers.update({row[k]:k})

            for row in reader:
                if (row[headers["EVENT"]] == "send"):
                    messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers[time_type]]))
                if (row[headers["EVENT"]] == "multisend"):
                    messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers[time_type]]))         
                    messages.append(Message(row[headers["TARGET2"]], row[headers["ID"]], row[headers[time_type]]))

    messages.sort(key= lambda m: m.send_time)

    # process receives
    for i in range(3):
        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                if (row[headers["EVENT"]] == "received"):

                    # grab the next message that is intended for this target and hasn't been received yet
                    message = None
                    for m in messages:
                        if int(m.receiver) == i and int(m.receive_time) == -1:
                            message = m
                            break
                    message.receive_time = int(row[headers[time_type]])

    latest = max([max(messages, key=lambda m: m.receive_time).receive_time, max(messages, key=lambda m: m.send_time).send_time])

    return messages, latest


def make_figure(time_type, time_label):
    messages, latest = load_data(time_type)
    latest += 2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0,latest)
    ax.set_ylim(0,10)
    ax.get_yaxis().set_visible(False)

    # draw lines
    xmin = 0
    xmax = latest
    y = 0
    height = 1

    # add process lines
    for i in range(3):
        y = y + 2.5
        plt.text(xmin - 0.1*(xmax-xmin), y, f"VM {i}")
        plt.hlines(y , xmin, xmax, label=f"VM {i}")
        plt.vlines(xmin, y - height / 2., y + height / 2.)
        plt.vlines(xmax, y - height / 2., y + height / 2.)

    # add events
    for message in messages:
        plt.plot(message.send_time, (message.sender+1)*2.5, 'ro', ms=5, mfc='r')
        if message.receive_time > -1:
            plt.plot(message.receive_time, (message.receiver + 1) *2.5, 'bo', ms=5, mfc='b')
            dx = message.receive_time - message.send_time
            dy = (message.receiver+ 1) *2.5 - (message.sender+1)*2.5
            plt.arrow(message.send_time, (message.sender+1)*2.5, dx, dy, head_length=(xmax-xmin)*0.01, head_width = 0.2, length_includes_head=True)

    plt.xlabel(time_label)
    plt.title("Space Time Diagram for Message Sends and Receives")

    plt.show()

if __name__ == '__main__':
    make_figure("LOGICAL_TIME", "Logical Time")
    make_figure("TIME", "Seconds Elapsed")
