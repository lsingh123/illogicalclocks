# illogicalclocks

### To run:

Your machine will need to have Python 3 (runnable by the `python3` command) as well as Flask within Python 3. To download flask, you can do `pip3 install flask requests`. You may have to do `pip install flask requests`, depending on if python3 is linked to pip or pip3. If you run into issues, see [this guide](https://flask.palletsprojects.com/en/1.1.x/installation/). You will also need to have ports 5000, 5001, and 5002 available.

To run three virtual machines communicating with each other, run: 

`bash run.sh`

To run the machines at a faster clock speed, you can do:

`bash run_fast.sh`

To run a single machine, you can do `python3 server.py`. However, this will fail because the server doesn't have any other servers running that it can communicate with.

To kill the machines after the `run` or `run_fast` command, you can do:

`bash kill.sh`

### Experiments and Design:

See the documents in the `docs/` folder for our experiment write up and our design decisions. You can also see the plots for each trial of our experiment in the `plots/` folder.

### Testing:

To run the tests, you can run:

`bash test.sh`

The test will run one machine as it receives mock time updates and performs deterministic send, multisend, and internal events. 

Experiment files are located in the `tests/` folder. 

The first line should be a space-separated line of integers. The first number is the clock frequency, typically "1" during tests. The next numbers represent an event. If the number is a "0", then the next number represents receiving a message with that next number as the time from another machine. Otherwise, the number represents a send or internal event. A "1" represents sending to one machine, a "2" represents sending to the other machine, a "3" represents sending to both machines, and anything else is an internal event.

The second line is the expected clock time after each event specified in the first line.

The third line is the expected action produced by each event from the first line.

To add your own test, you can add a test file to the `tests/` folder called `xxxx`, then you can add to the end of `test.sh` (before the final `rm` command) `python3 code/server.py -t ./tests/xxxx -id 2 -s 60 && python3 code/testeval.py -expected ./tests/xxxx`.


