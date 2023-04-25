# Industrial Reconstruction using py-openshowvar (kuka var proxy)

## Description

This repo contains a docker container for running the [industrial reconstruction](https://github.com/ros-industrial/industrial_reconstruction) on KUKA robots. Kuka var proxy and py-openshowvar are used to communicate with the robot controller. 

Contents of container

- ROS noetic
- industrial-reconstruction
- ros-osv (py-openshowvar)
- ros-realsense (with D405 wrapper for ROS1)

## Docker

### Installation

Follow the instructions on the [docker website](https://docs.docker.com/engine/install/ubuntu/) to install docker on your system. its recommended to complete the linux [post installation instructions](https://docs.docker.com/engine/install/linux-postinstall/) as well.

For Nvidia support follow the instructions on the [nvidia website](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) to install the nvidia docker runtime.

### Build

This repo provides convenience shell scripts to build and run the docker container. To build the container run the following command from the root of the repo:

```bash
.docker/build_image.sh
```

### Run

To run the container run the following command from the root of the repo:

```bash
.docker/run_user.sh
```

or if you have a nvidia gpu and have installed the Nvidia container toolkit run:

```bash
.docker/run_user_nvidia.sh
```

This will start the container and mount the home directory and user to the container. The container will also be run in interactive mode so you can use the terminal in the container. Terminator installed in the container so you can open multiple terminals in the container, run ```terminator``` to open terminator once inside the container.

You will not own the catkin workspace in the container so you will need to run ```sudo chown -R $USER /dev_ws``` to change the ownership of the catkin workspace to your user.

If you want the workspace to be sourced automatically when you open a new terminal in the container you can add the following line to your ```.bashrc``` file on the host machine:

```bash
if [ -f "/dev_ws/setup.bash" ]; then
    source /dev_ws/setup.bash
fi
```

## References

- [industrial reconstruction](https://github.com/ros-industrial/industrial_reconstruction)  
- [realsense-ros](https://github.com/rjwb1/realsense-ros)  
- [kuka var proxy](https://github.com/ImtsSrl/KUKAVARPROXY)
