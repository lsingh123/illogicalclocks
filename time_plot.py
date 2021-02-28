import matplotlib.pyplot as plt
import csv

'''
This file generates clock drift graphs using 0.txt, 1.txt, and 2.txt as input data
'''

'''
load_data: None -> int[][][] times, int[] rates
reads in data from input files and produces a single array of logical and system time for each VM
and a single array containing the clock tick rates for each VM
'''
def load_data():

    times = [[[], []], [[], []], [[], []]]
    rates = [1, 1, 1]
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
                rates[i] = row[headers["RATE"]]
    return times, rates

'''
make_plot(): None -> None
draw the plot
'''
def make_plot():

    data, rates = load_data()
    colors = ["red", "green", "blue"]
    groups = [f"VM 0 ({rates[0]} t/s)", f"VM 1 ({rates[1]} t/s)", f"VM 2 ({rates[2]} t/s)"]

    # create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # add points
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


