# Experimental Results 

## Experimental Setup

We ran each experiment with 3 virtual machines for 4 minutes at a time. Trial 1-5 ran the machines for 4 minutes. Trials 6-7 
reduced the probability of an internal event to 1/2, and Trials 8-9 reduced this probability further to 3/10. Tick rates were 
initialized randomly. This report will include plots we found especially interesting. To see all data, go to `plots/` 
The code that generated these plots is in `code/` `code/spacetime_plot.py` generated the spacetime diagrams and `code/time_plot` generated the clock drift graphs.

We made three kinds of plots for each trial. 

1. **Clock Drift Graph** These diagrams have system time, measured in seconds elapsed since start on the x-axis and logical time on the y-axis. Each virtual 
machine is a different color, and the scattplot shows logical time as a function of system time. The blue lines on these plots represent zero drift, as in 
logical time = system time. Because our machines are really slow (only a few ticks per second), they all have far lower logical time than the hypothetical
zero drift clock. 

As an example, here's the Clock Drift graph for Trial 4:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%204/drift.png)

2. **Logical Space Time Diagram** This is a space time diagram using logical time. Each virtual machine is represented by a horizontal line. Green circles 
represent internal events, red circles represent message sends, and blue circles represent message receives. Arrows connect sends to receives, and sends without
an arrow weren't received at all. 

As an example, here's the Logical Space Time diagram for Trial 4:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%204/space_logicaltime.png)

3. **System Space Time Diagram** This is a space time diagram using system time (measured in seconds elapsed since start) instead of logical time. This diagram
is helpful to see the jump in logical time value. Arrows with steeper slopes indicate smaller jumps in logical clock values, and therefore more synchronized
clocks. The arrows on logical space time diagrams tend to have similar slope, where as system space time diagrams show some distortion in arrows depending 
on differences in tick rate.

As an example, here's the System Space Time Diagram for Trial 4:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%204/space_systemtime.png)

### Observation 1: Faster Clocks Drift Less

The first observation is that faster clocks, as in clocks with a higher tick rate, drift less from system time. The clock drift diagram below for Trial 1 demonstrates this fact. The blue line represents a clock with no drift from system time, and the dots represent logical vs system time for different VM's. 

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%201/drift.png)

Notice that VM 1, represented by the green dots, drifts the least from system time, whereas VM 2, represented by blue dots drifts the most. VM 1's tick rate is four times that of VM 2, hence the difference in drift.

Trial 5's drift diagram demonstrates this fact even more dramatically. The green machine has a tick rate of 6 ticks/second, and thus drifts far less than the blue and red 
machines, which have tick rates of 1 tick/second. 

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%205/drift.png)

This implies that if components in a distributed system must be synchronized with some real time clock, they should acheive tick rates 
as close as possible to the "real" clock tick rate. Note that for the purposes of our experiment, a higher tick rate also meant more 
data points to plot and analyze, which produced some cleaner looking lines on the scatterplot. If we ran our trials for far longer, maybe 30 minutes, then the noise should fade away and all three VM's, regardless of tick rate, should achieve similarly clean lines.

### Observation 2: Receivers are Receivers/ Message Queue Length

In Trial 9, VM sends a bunch and the other guys get clogged and can't send anymore -> mention connection between clock speed and length of the message queue

### Observation 3: Higher probability of message send

Trial 1 and Trial 8 have same tick rates but diff probabilities of message send

### Observation 4: Variance in Clock Tick Rate == Higher Jumps in Logical Clock Times

Trial 1 space time diagram for logicaltime vs systemtime vs Trial 2

### Observation 5: Same Clock tick rate == Same Drift

The boring trial 2. 

### Observation 6: Slower clocks have higher jumps in logical clock value

Trial 4 space time diagrams 











