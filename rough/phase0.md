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

This is similar to pickle library, but works for closures, functions and decorators. 
