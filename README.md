# What is this? #

This is an example project for running Jupyter Hub via docker on systems with multiple GPUs.

The design goal is that Jupyter Hub will run in a container that has access to the hosts docker system in order to spawn the single user servers in their own containers with configurable access to the system's GPUs.

## Jupyter Hub Configuration options: ##
### Authentication ###
Jupyter Hub by default will authenticate users using the local system's facilities. However, since this project aims to run Jupyter Hub in a container the `/etc/passwd`, `/etc/shadow`, and `/etc/group` files of the underlying system are unavailble, as is the PAM system from the host.

> Currently this project is bind mounting these files into the hub container so that local system users can login to test the functionality.

Other authentication options that I need to explore include LDAP, FreeIPA (or Red Hat IdM), and Active Directory.

### Spawner ###
This project is currently using the `dockerspawner.DockerSpawner` spawner. I need to look more into the `dockerspaner.SystemUser` spawner too as it may more closely align with my design goals.

### Single User Environment ###


### Proxy ###

## GPU allocation ##
Using the `--gpus` flag with docker is how access to GPUs is requested. 

Example: Requesting all GPUs
```shell
docker run --gpus 'all,capabilities=utility' --rm ubuntu nvidia-smi
```

Example: Requesting 2 GPUs[^quantiy_by_number]
```shell
docker run --gpus '2,capabilities=utility' --rm ubuntu nvidia-smi
```

Example: Requesting a single specific GPU by position
```shell
docker run --gpus 'device=2,capabilities=utility' --rm ubuntu nvidia-smi
```

Example: Requesting 2 specifig CPUs by position
```shell
docker run --gpus '"device=0,2",capabilities=utility' --rm ubuntu nvidia-smi
```

Example: Requesting a single specifig GPU by uuid
```shell
docker run -it --rm --gpus device=GPU-711c12b7-d90f-a41c-ad1d-07017ee178fc ubuntu nvidia-smi
```

Exmaple: Requesting 2 specific GPUs by uuid
```shell
docker run -ti --rm --gpus '"device=GPU-711c12b7-d90f-a41c-ad1d-07017ee178fc,GPU-8b1cf8a5-7a04-ac63-0be8-c52f43bf326a",capabilities=utility' ubuntu nvidia-smi
```

The problem with simply requesting a number of GPUs for each single user environment is that, in my testing, docker will allocate the same GPUs over and over. If one GPU is requested by 5 containers they will all get the same GPU (the first one enumerated in the host system). 

Some way to track and allocate GPUs is needed.

[^quantity_by_number]: I've noticed that this isn't really talked about in the docker documentation. I confirmed that it works by testing it, but this may not be a reliable way to request a number of GPUs.
### The GPU Allocator ###

The GPU Allocator is a simple api that I've written using flask. Using it's REST API i can be populated with a list of uuids, which it will store and track. Before launching a single user server it can be querried for an available gpu uuid that can be requested when creating the new single user server container.

The allocator will increment a counter and when all GPUs are in use it will return an error.

It can be configured to allow over subscription by setting an integer value for how many times a particular GPU can be allocated. When oversubscription is enabled the allocator will still return the least used GPU (or the first GPU with the lowest useage encountered)

Usage is calculated only by number of times it's been allocated, currently there's no way of the allocator to know how much acutal load is placed on the GPU.

## Present state of the project: ##

Docker compose is used to start the hub service. 

### Things which need to be done: ###

* Develop a good way to populate the gpu allocator with available hardware.
* Implement usage of the gpu_allocator in the jupyterhub config.
* Test GPU allocation on a multi-gpu system.
* Investigate other spawners.
* Investigate other authentication methods.
* De-allocate GPUs on exit.
* Find a method to ensure single user servers don't stay around when idle.