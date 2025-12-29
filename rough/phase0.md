# Learnings from phase 0

# Docker ( Small Cheat Sheet )
## docker cli flags 

- to build an image from a dockerfile 
```bash
docker build -t <image_name> .
```

- building a docker image from a dockerfile without the cache
```bash
docker build --no-cache -t <image_name> .
```

- list docker images 
```bash
docker images
```

- delete docker image 
```bash
docker rmi <image_name>
```

- remove all the unused docker images 
```bash
docker image prune
```

What is the difference between rmi and prune in docker ?
> Prune removes unused images, while rmi removes a specific image.

## Docker Hub

This is a service provided by docker to store and share docker images with people around the world.

- Login to docker hub : docker login -u <username> -p <password> 
- publish an image to the docker hub : docker push <username>/<image_name> 
- search for a image on the hub : docker search <image_name>
- pull an image from the hub : docker pull <username>/<image_name>

## General Commands 

- start the docker deamon : docker -d 

## Containers 

Containers are runtime instances of docker image. A container will always run the same, regardless of the infrasturcture available.
Containers isolate software from the environment it is running and ensure that it works uniformly across different environments despite the differences present between environments.

- create and run a container from a image with a custom name
```bash
docker run --name <container_name> <image_name>
```

- Run a container with and publish a container’s port(s) to the host.
```bash
docker run -p <host_port>:<container_port> <image_name>
```

- Run a container in the background
```bash
docker run -d <image_name>
```

- Start or stop an existing container:
```bash
docker start|stop <container_name> (or <container-id>)
```

- Remove a stopped container:
```bash
docker rm <container_name>
```

- Open a shell inside a running container:
```bash
docker exec -it <container_name> sh
```

- Fetch and follow the logs of a container:
```bash
docker logs -f <container_name>
```

- To inspect a running container:
```bash
docker inspect <container_name> (or <container_id>)
```

- To list currently running containers:
```bash
docker ps
```

- List all docker containers (running and stopped):
```bash
docker ps --all
```

- View resource usage stats
```bash
docker container stats
```

## cloudpickle

This is similar to pickle library, but works for lambdas, closures, functions and decorators. 

.dumps() to serialize the data - use cloudpickle for serializing 
.load() to deserialize the data - use cloudpickle for deserializing

### *args and **kwargs in python - super common but often confused by people 
>small recap:

- It allows functions to accept any number of arguements.
    - args = Positional Arguements
        function(1,2,3) , here the (1,2,3) is converted to a tuple when passed as *args
        the variables are bundleled as a tuple, inside the function args becomes (1,2,3)
 
    - kwargs = Keywords Arguements
        take all the named arguements and bundle them as a dictionary named kwargs 
        function(a=1,b="hello"), then kwargs becomes {'a': 1, 'b': 'hello'}.

Why is this needed in nano-modal? 
User defined functions can have any arguements passed to the function. We need to extract them without fail to ensure the function runs as programmed by the user.
We can package the arguements as bytestream and send them to the worker

# tests

completed writing a simple test function to test serialize and deserialization


# step 0.3
Step 0.3: app.py

App class with name parameter
functions dict to store registered functions
function() decorator method
Wrap function in Function object
Return wrapped function

the goal of this task must be: 
```python 
@app.function()
def fxn(x):
    return x*2
```

create this structure so that the syntax works

# grpc 

grpc is like the "contract" between the server and the client

# Proto file

this file tells the protocol buffers that we are using the version 3 of the syntax

- declare the service with 2 RPC methods : invoke and getresult 
invoke = sends a function to execute and gets back task id 
getresult = asks for result using that task ID

invoke = invoke request and invoke response ( get back task ID ) 

getresult = getresultrequest and getresultresponse

What This Defines:

NanoModal service - the API your server will implement
Invoke RPC - client sends function to execute
GetResult RPC - client asks for result
Messages - the data structures for communication
Key Concepts:
bytes - for your cloudpickle serialized data
string - for task IDs and error messages
rpc - remote procedure call (function call over network)
