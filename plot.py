import matplotlib.pyplot as plt
import csv


events = [[], [], []]
events[0] = [1, 2, 3, 4]
events[1] = [3, 5, 6]
events[2] = [0, 2, 4, 6]

class Message:

    def __init__(self, receiver, sender, time_sent, time_received):
        self.sender = sender
        self.receiver = receiver
        self.send_time = time_sent
        self.receive_time = time_received

def load_data():
    messages = []
    latest = 0
    
    # process sends
    headers = {}
    for i in range(3):
        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            headers = {}

            for row in reader:
                if (len(headers) == 0):
                    for k in range(len(row)):
                        headers.update({row[k]:k})
                else:
                    if (row[headers["EVENT"]] == "send"):
                        if int(row[headers["LOGICAL_TIME"]]) > latest:
                            latest = int(row[headers["LOGICAL_TIME"]])
                        messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers["LOGICAL_TIME"]], -1))
                    if (row[headers["EVENT"]] == "multisend"):
                        if int(row[headers["LOGICAL_TIME"]]) > latest:
                            latest = int(row[headers["LOGICAL_TIME"]])
                        messages.append(Message(row[headers["TARGET1"]], row[headers["ID"]], row[headers["LOGICAL_TIME"]], -1))         
                        messages.append(Message(row[headers["TARGET2"]], row[headers["ID"]], row[headers["LOGICAL_TIME"]], -1))

    # process receives
    for i in range(3):
        with open(f"{i}.txt", "r") as f:
            print(f"processing file {i}")
            reader = csv.reader(f, delimiter=",")
            count = 0
            for row in reader:
                if count == 0:
                    count += 1
                else:
                    if (row[headers["EVENT"]] == "received"):
                        if int(row[headers["LOGICAL_TIME"]]) > latest:
                            latest = int(row[headers["LOGICAL_TIME"]])

                        # grab the next message that is intended for this target and hasn't been received yet
                        message = None
                        for m in messages:
                            if int(m.receiver) == i and int(m.receive_time) == -1:
                                message = m
                                break
                        message.receive_time = int(row[headers["LOGICAL_TIME"]])


    return messages, latest


def draw_arrow(x, y, x_end, y_end):
    plt.arrow(x, y, x_end-x, y_end-y, 
          head_length=.2, head_width=.2,
          length_includes_head=True)

messages, latest = load_data()
latest += 2
# set up the figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0,latest)
ax.set_ylim(0,10)

# draw lines
xmin = 0
xmax = latest
y = 0
height = 1

for i in range(3):
    y = y + 2.5
    plt.text(xmin, y+0.3, f"Process {i}")
    plt.hlines(y , xmin, xmax, label=f"Process {i}")
    plt.vlines(xmin, y - height / 2., y + height / 2.)
    plt.vlines(xmax, y - height / 2., y + height / 2.)

for message in messages:
    plt.plot(int(message.send_time), (int(message.sender)+1)*2.5, 'ro', ms=5, mfc='r')
    plt.plot(int(message.receive_time), (int(message.receiver) + 1) *2.5, 'bo', ms=5, mfc='b')
    dx = int(message.receive_time) - int(message.send_time)
    dy = (int(message.receiver) + 1) *2.5 - (int(message.sender)+1)*2.5
    plt.arrow(int(message.send_time), (int(message.sender)+1)*2.5, dx, dy, head_length=0.2, head_width = 0.2, length_includes_head=True)

plt.xlabel("Logical Time")

plt.show()
