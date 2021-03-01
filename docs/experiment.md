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

### Observation 2: Receivers Stay Receivers

Consider the following space-time diagram for Trial 9. 

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%209/space_logicaltime.png)

The probability of message sends is quite high (7/10) for all VM's, but VM 0 has a tick rate of 5 ticks/second, whereas VMs 1 and 2 have tick rates of 1 
tick/second. VM 0 sends a bunch of messages over really quickly, so VM1's and VM0's message queues become very long. Because their message queues are very 
long, they are stuck simply receiving messages, so VM0 never receives anything, so it keeps sending more messages and the cycle continues. 

In particular, VM's with a faster tick rate have shorter message queues because they can process messages more quickly, and because they can make more sends
before the others have the chance to send a single message out. VM's with slower tick rates have longer message queues because they are slow to process 
messages and become inundated quickly. Thhis observation is supported by comparing the diagram above, which uses logical time, to the diagram below, which uses
system time. VM 2 and VM 1 appear to be idle in the diagram above because such few events happen, but the diagram below demonstrates that these events are 
distributed quite sparsely across system time because the tick rates are so slow.

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%209/space_systemtime.png)

### Observation 3: Changing Probability of Message Send

Trials 1 and 8 have three machines with the same tick rates (1 tick/second, 2 ticks/second, 4 ticks/second), but Trial 8 has a far higher (7/10 compared to
3/10) probability of an event being a message send instead of an internal event. Below is the clock drift graph for Trial 1:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%201/drift.png)

And for Trial 8:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%208/drift.png)

Notice that the drift rates appear to be similar for both trials, but Trial 8 has far cleaner lines because there are more datapoints because there are more 
logged events because there are more messages being exchanged. VM 0 (red) in Trial 1 (first graph) appears to have far less drift than expected, but this could
also be due to noise since VM 0 has logged fairly few events. 

Also compare the spacetime diagram for Trial 1:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%201/space_logicaltime.png)

And for Trial 8:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%208/space_logicaltime.png)

In Observation 2, we claimed that machines with faster tick rates will inundate the others with messages and the others will get stuck with long message queues,
just processing messages. This property appears to be far stronger with a higher probability of an event being a message send (Trial 8, second graph), as 
evidenced by VM 2 dominating Trial 8's space time diagram. This makes sense because there is a higher probability that Trial 8 uses its faster tick rate to 
send a bunch of messages to the others instead of performing internal events.

Trial 8 in particular had a really high probability of multisends, so messages sent simultaneously to both of the other VMs. This explains why, in the Trial 8
diagram, VM 1 and VM 0 appear to receive messages at a similar logical clock rate. Note that VM 1 stops receiving messages sooner because its tick rate is 
slower, so system time runs out sooner for it. This is clearest when looking at the space system time diagram for Trial 8:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%208/space_systemtime.png)


### Observation 4: Variance in Clock Tick Rate => Jumps in Logical Clock Times

Trials 1 and 2 have the same probability of internal events (7/10) but Trial 1 machines exhibit variance across tick rate (4 ticks/second, 2 ticks/second, 1
tick/second) where as all three Trial 2 machines have the same tick rate (1 tick/second). 

Here is the space logical time diagram for Trial 1:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%201/space_logicaltime.png)

And for Trial 2:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%202/space_logicaltime.png)

There are far fewer events in Trial 2 because of the slower tick rate. Because all three clocks have the same tick rate, notice that the jumps in logical time
value, as indicated by space between event circles, are the same. For Trial 1, VM 1 and VM 2 display far bigger jumps in logical clock value because they are 
slower than VM 4. The average size of logical time jump appears to the same for each Trial, but Trial 1 exhibits more variance in logical clock jumps because 
of the varying tick rates across machines. In Trial 1, the slow VM 2 in Trial 1 processes messages that the fast VM 1 sent far far in the future. In Trial 2, 
all machines send and process at the same rate.

### Observation 5: Same Clock Rate => Same Drift

In Trial 2, all VMs had the slow tick rate of 1 tick/second. The drift diagram for Trial 2 is below:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%202/drift.png)

Notice that the drift rates are all the same! Each VM processes exactly 4 events and these are all processed at the same system time. Machines with the exact 
same tick rate have the exact samr drift amount and frequency of logical clock update. This observation supports the running theme that properties we care about
in a distributed system, like logical time jumps and clock drift, depend on *relative* tick rates, not absolute tick rates. Higher variance in tick rates leads 
to undesirable properties like logical time jumps and clock drift.


### Observation 6: Slower Machines Jump More and Have Larger Message Delays

Trial 4 showed us that VMs with slower tick rates display larger jumps in logical time values. Consider the space logical time diagram below:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%204/space_logicaltime.png)

VM 2 and VM 0 have similar tick rates (6 ticks/second and 5 ticks/second) and VM 1 has a far slower tick rate (1 tick/second). The slower machine has far 
greater jumps in logical clock value, as demonstrated by the distance between events for VM 1. 

Additionally, consider the system space time diagram below:

![image](https://github.com/lsingh123/illogicalclocks/blob/main/plots/Trial%204/space_systemtime.png)

The slope of the arrows denotes the delay between message send and receipt. Notice that messages sent between VM 0 and VM 2, who have similar tick rates have
arrows with steeper slope, and thus less delay between message send and receipt. On the other hand, VM 1 exhibits large delays when receiving from VM 0 and VM 
2 because it is slow. The logical space time diagram obscures this detail because logical time is generally lower and less fine-grained (since we only have a 
few events per second). Details like slopes are exaggerated in system time diagrams.

## Conclusions

There are a few properties that might be useful in a distributed system, and this experiment revealed how clock tick rates affect them. First, jumps in 
logical clock values, also known as jumping forward in time, might be considered undesirable. These are caused by variances in clock tick rates. When talking 
to a faster VM, the slower machine sees larger jumps in logical clock values. Second, clock drift is generally considered problematic. Clock drift from "real" 
or system time occurs more in slower VM's, but all time is relative, especially in a distributed system. In the absence of God's eye views of time, relative 
clock drift is most important, and this can be avoided by machines that tick at similar rates. Third, long message queues prevent machines from doing tasks 
other than message processing. Slow machines talking to fast machines tend to suffer from long message queues. 









