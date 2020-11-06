[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Reverse Shell For C&C In Python With Extended Functionality


### PROBLEM STATEMENT
In this project, we have created a *Reverse Shell for C&C in Python* with extended functionalities. A reverse shell is a type of shell in which the target machine communicates back to the attacking machine. The attacking machine has a listener port on which it receives the connection, which by using, code or command execution is achieved. In our project we have tried to go a step further and add a bit more functionality to our program to add more features to the standard reverse shell.
![screenshot](/Images/img.jpeg)
 
For example –  An attacker wants to perform post exploitation kung-fu on a compromised machine. A standard reverse shell would be limited to primitive command execution. Often , STDERR can terminate the remote session, which isn't a favourable scenario for a hacker. Here we have tried to solve these problems and provide a more stable C&C framework.

### OVERVIEW-
We have created 2 sets of programs -

```
[+] One to handle Server Side connections
[+] One to handle Client Side connections
```

The Client Side Program has the IP, Port pair of the Hacker’s machine or an equivalent proxy connection. The Client side program initiates a connection to the Hacker’s (Server) computer. The Hacker listens for an incoming connection from the victim at the specified port and on incoming requests, validates the connection via a password. Once connected, the attacker can drop a shell with the privileges of the user with which the Client Side program was triggered.With the help of Reverse Shell, the following tasks can be done :-

```
[+] Executes Commands On Victim
[+] Upload Files On Victim
[+] Download Files From Victim
[+] Capture Screenshot
```

### MOTIVATION FOR CHOOSING THIS PARTICULAR TOPIC FOR THE PROJECT-
In Cyber security it is often noticed that Reverse Shells have a remediate functionality. So we have tried to create a combined solution which allows us to do multiple tasks on the victim’s machine.  standard reverse shell would be limited to primitive command execution. Often , STDERR can terminate the remote session, which isn't a favourable scenario for a hacker. Here we have tried to solve these problems and provide a more stable C&C framework.

### Note :

For the Screenshot feature to work , scrot must be installed on the Victim  !
