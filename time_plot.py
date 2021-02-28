import matplotlib.pyplot as plt
import csv
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

def load_data():

    times = [[[], []], [[], []], [[], []]]
    for i in range(3):

        with open(f"{i}.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            
            # populate headers to make future row indexes easier
            headers = {}
            row = next(reader)
            for k in range(len(row)):
                headers.update({row[k]:k})
             
            for row in reader:
                times[i][1].append(int(row[headers["LOGICAL_TIME"]]))
                times[i][0].append(int(row[headers["TIME"]]))
    return times 

def make_plot():

    data = load_data()
    colors = ["red", "green", "blue"]
    groups = ["VM 0", "VM 1", "VM 2"]

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(3):
        ax.scatter(data[i][0], data[i][1], c=colors[i], label=groups[i])

    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))

    # plot y=x as a control line
    x_min, x_max = ax.get_ylim()
    ax.plot([x_min, x_max], [x_min, x_max], label="No Drift")    

    plt.xlabel("Seconds Elapsed")
    plt.ylabel("Logical Time")
    plt.title('Clock Drift')
    plt.legend(loc=2)
    plt.show()
 
if __name__ == '__main__':
    make_plot()


