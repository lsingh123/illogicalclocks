# Experimental Results 

## Experimental Setup

We ran each experiment with 3 virtual machines for 4 minutes at a time. Trial 1-5 ran the machines for 4 minutes. Trials 6-7 
reduced the probability of an internal event to 1/2, and Trials 8-9 reduced this probability further to 3/10. Tick rates were 
initialized randomly. This report will include plots we found especially interesting. To see all data, go to `plots/` 
The code that generated these plots is in `code/` `code/spacetime_plot.py` generated the spacetime diagrams and `code/time_plot` generated the clock drift graphs.

### Observation 1: Faster Clocks Drift Less

The first observation is that faster clocks, as in clocks with a higher tick rate, drift less from system time. The clock drift diagram below for Trial 1 demonstrates this fact. The blue line represents a clock with no drift from system time, and the dots represent logical vs system time for different VM's. 

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%201/drift.png?s=200)

Notice that VM 1, represented by the green dots, drifts the least from system time, whereas VM 2, represented by blue dots drifts the most. VM 1's tick rate is four times that of VM 2, hence the difference in drift.

Trial 5's drift diagram demonstrates this fact even more dramatically. The green machine has a tick rate of 6 ticks/second, and thus drifts far less than the blue and red 
machines, which have tick rates of 1 tick/second. 

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%205/drift.png)

This implies that if components in a distributed system must be synchronized with some real time clock, they should acheive tick rates 
as close as possible to the "real" clock tick rate. Note that for the purposes of our experiment, a higher tick rate also meant more 
data points to plot and analyze, which produced some cleaner looking lines on the scatterplot. If we ran our trials for far longer, maybe 30 minutes, then the noise should fade away and all three VM's, regardless of tick rate, should achieve similarly clean lines.

### Observation 2: Receivers are Receivers

In Trial 9, VM sends a bunch and the other guys get clogged and can't send anymore 

### Observation 3: Higher probability of message send

Trial 1 and Trial 8 have same tick rates but diff probabilities of message send

### Observation 4: Variance in Clock Tick Rate == Higher Jumps in Logical Clock Times

Trial 1 space time diagram for logicaltime vs systemtime vs Trial 2

### Observation 5: Same Clock tick rate == Same Drift

The boring trial 2. 











