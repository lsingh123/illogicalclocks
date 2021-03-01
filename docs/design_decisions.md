# Design Decisions

#### 1: Use `flask` to handle our server-side networking.

Flask is a python package that helps you quickly set up HTTP servers. Using HTTP allowed us to not worry about persistent connections with sockets. The server could simply receive a time update from another machine, then put that update on the networking queue for the VM to handle. By using a package to handle server-side networking, we didn't have to spend time worrying about socket protocols and all of the messy errors that can crop up there.

#### 2: Use `requests` to handle our client-side networking.

Similar to the first decision, by using an external library to handle our HTTP requests, we saved a lot of time dealing with messy socket code. With this decision, we only had to write one line of client-side networking code, which was a simple get request.

#### 3: Pass the time within the HTTP request as the route.

Rather than using the traditional method of encoding a machine's time as a `GET` request parameter, we allowed a VM to receive a time from another machine by simply receiving a get request at its `/x` url, where `x` was the time it was receiving. This is a feature of Flask that is usually used for indexing different types of content with an id. For example, a social media site might have a `/posts/x` route to direct a user to a webpage for post x. This method allowed us to quickly receive the number from the request then immediately put it on the queue, rather than worrying about parsing the parameters of the request.

#### 4: We used two threads: one for receiving time updates from other machines, the other for handling the logic of the machine. To communicate, they use a thread-safe queue.

Because the VM is supposed to have a limited clock cycle, but it should be able to receive network messages at any time. To meet this requirement, we had the thread for the VM sleep for the specified amount of time, then "wake up" and do its operations. Independent of this, a separate thread would always be awake, and would just add received messages to the queue whenever one came in. If there was a message available on the queue, the VM thread would receive it once it woke up. The only issue with this method is that we could not run the flask servers in development mode because it is not thread safe.

#### 5: To test, we allowed the tester to specify the sequence of sends/receives the VM would take and make sure that the logical time was updated correctly.

