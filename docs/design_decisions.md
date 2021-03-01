# Design Decisions

#### 1: We used `flask` to handle our server-side networking.

Flask is a python package that helps you quickly set up HTTP servers. Using HTTP allowed us to not worry about persistent connections with sockets. The server could simply receive a time update from another machine, then put that update on the networking queue for the VM to handle. By using a package to handle server-side networking, we didn't have to spend time worrying about socket protocols and all of the messy errors that can crop up there.

#### 2: We used `requests` to handle our client-side networking.

Similar to the first decision, by using an external library to handle our HTTP requests, we saved a lot of time dealing with messy socket code. With this decision, we only had to write one line of client-side networking code, which was a simple get request.

#### 3: We passed the time within the HTTP request as the route.

Rather than using the traditional method of encoding a machine's time as a `GET` request parameter, we allowed a VM to receive a time from another machine by simply receiving a get request at its `/x` url, where `x` was the time it was receiving. This is a feature of Flask that is usually used for indexing different types of content with an id. For example, a social media site might have a `/posts/x` route to direct a user to a webpage for post x. This method allowed us to quickly receive the number from the request then immediately put it on the queue, rather than worrying about parsing the parameters of the request.

#### 4: We used two threads: one for receiving time updates from other machines, the other for handling the logic of the machine. To communicate, they use a thread-safe queue.

Because the VM is supposed to have a limited clock cycle, but it should be able to receive network messages at any time. To meet this requirement, we had the thread for the VM sleep for the specified amount of time, then "wake up" and do its operations. Independent of this, a separate thread would always be awake, and would just add received messages to the queue whenever one came in. If there was a message available on the queue, the VM thread would receive it once it woke up. The only issue with this method is that we could not run the flask servers in development mode because it is not thread safe.

#### 5: To test, we allowed the tester to specify the sequence of sends/receives the VM would take and make sure that the logical time was updated correctly.

Because we were ultimately concerned with each machine keeping its own logical time, we could test that each machine was keeping time correctly by simulating received messages and pre-specifying the otherwise "random" action the VM would take when it had no messages available. This method allowed us to specify complicated send/receive sequences that we would be unlikely to see at random to ensure that the VM behaved appropriately in those scenarios.

#### 6: To run and kill the machines, we built bash scripts.

For the sake of isolation, we wanted each VM to have its own process ID on the host machine. While we probably could have built a separate python script to fork off each process and have those machines communicate with each other, this seemed like overkill when running multiple python3 programs could easily be accomplished with a bash script. We did run into issues, at first, in trying to kill the background python processes, but we ultimately had success with the `pkill` unix command. The bash script abstracted away the longer, mildly complicated command of running each server program in the background with a different id.

#### 7: We had each machine use a different port on localhost.

Using multiple ports allowed us to run the exact same server multiple times on the same OS. From the eyes of each virtual machine, it had a full server that could be accessed by any process on the machine wanting to use localhost.

#### 8: We used the csv file format for our logs.

Though our files had the ".txt" file extension, they were formatted as CSV files. Using the CSV format allowed us to quickly analyze the data from our experiements. It also allowed us to easily build graphs for those experiments.

