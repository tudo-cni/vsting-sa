
# vSTING-SA (Non-Final)
**virtual Spatially distributed Traffic and INterference Generator - Standalone**

*This work has been supported by the German Center for Rescue Robotics (DRZ)
and funded by the German Federal Ministry of Education and Research (BMBF)
in projects A-DRZ (13N14857) and DRZ (13N16476).*

[[_TOC_]]

## 1. Introduction

The vSTING is a solution for evaluating teleoperated robots and other network reliant systems or applications in challenging network environments such as ones with heavy traffic or interference. It is adjusted for practical usage and ease of installation for system evaluations and experiments.

## 2. How it works

vSTING uses network emulation to recreate degraded network environments. One main advantage is the lack of additional software installation on the evaluated systems. vSTING runs on a separate device tasked with encapsulating the network degradation.
The vSTING device must be installed between operator and robot to introduce network degradation on the communication link between them. The resulting architechture  is illustrated in Fig. 1

![The vSTING concept\label{fig:vsting-concept}](figs/vsting-concept.png)

<!-- <img src="figs/vsting-concept.svg" width="70%"> -->

This results in a hardware requirement for the device on which vSTING is installed: it must feature at least two RJ45 ports to be able to support the two ethernet links meant for robot and operator. A third port can be required to stand for the control channel, to connect the device on which the vSTING user interface will be displayed. This link can however be also be realized in other ways, such as over WiFi. 


## 3. Installation

As mentionned previously, vSTING is a software solution running on adequately configured hardware. Two installation methods are supported:

- **installation on a supported device using system image**: This is the recommended installation method, since it requires less configuration steps. A system image is downloaded and installed on the device. After this, the vSTING is ready.

- **installation on custom devices**: This method requires additional configuration steps on your device and on the downloaded software bundle.


### 3.1 Installation tutorial on a supported device (using Ubuntu 20.04)

the software bundled was preconfigured and tested on some devices and system images ready to be used were created. The following indications were tested and are therefore supported for the following system:  

- [APU-4D4](https://www.apu-board.de/produkte/apu4d4.html)

The following materials are required for this tutorial:  

1. One mirco SD-card (at least class 10 and 16GB) with a micro-SD adapter  
2. One personal computer with ubuntu 20.04 to download and install the system image on the SD-card  
3. One APU 4D4  

![Required materials for the APU installation.](figs/materials-apu-install.png)

<!-- <img src="figs/materials.png" width="70%"> -->

The following instructions will guide you through the download of the vsting system image and its installation on your APU 4D4 to turn it in a vSTING device.

Starting on the personal computer:

- install packages required for the setup process:

        sudo apt install -y coreutils pv wget gzip git

- clone the vsting repository:

        git clone https://github.com/tudo-cni/vsting-sa.git

- enter the scripts folder found in the cloned folder, make the scripts executable and download the system image by running the download script:

        (cd vSTING-SA/scripts && chmod +x *.sh && ./download-image-apu4d4.sh)

  **NB**: *The image file's size is around 1.5GB, make sure you have enough free space on your system, and that you are not using a metered internet connection. The download may take more or less time depending on your internet speed.*

- insert the SD-card in the personal computer and make sure it is available. If it is, you should be able to find the sdcard device file in the `dev` folder. It usually starts  with either `mmcblk` or `sd`. you can also open the `disks` application and look for the sd-card device file as illustrated in Fig. \ref{fig:find-sd-card-device}  below:  

![Identify your SD-card device file \label{fig:find-sd-card-device}](figs/sd-card-check.png)

- install the vsting image on the sdcard by running the image installation script `install-image-apu4d4.sh` with your *sdcard device file* and the *downloaded image file's name* as arguments. This step can take a while.  
As an example, provided the sdcard device is `mmcblk0` and the image file is named `apu-vsting-sa.img.gz`, the command to run in your terminal would look like this: 

        ./install-image-apu4d4.sh /dev/mmcblk0 apu-vsting-sa.img.gz
  **NB**: *when calling the script with the arguments, the sdcard device comes first and the image file comes second. Misplacing the arguments could corrupt the image file. In this case, a new download is required.*

After the image is written to the SD-card, eject it from the computer:

- insert the SD-card in the APU 4D4 and power it up.

- connect your computer using an ethernet cable to the APU on the ethernet port `enp1s0` (the first one from the right while the APU is upside down, the closest one the  serial port and farthest from the USB ports). Fig.\ref{fig:apu-ports-annotated} below shows the annotated network ports of the APU 4D4.

![APU ports annotated\label{fig:apu-ports-annotated}](figs/apu-ports-annotated.png)

- give your computer the fixed ip `10.40.1.10` with network mask `/24` or `255.255.255.0` on the wired network interface. The annotated steps in [section 6.1](#61-set-a-static-ip-address-on-your-device)  might be of help.

- make sure the connection is effective by trying to reach the APU. The output of the following command should display the round-trip time to the APU:

        ping 10.40.1.1


Once you have ascertained that the connection is effective, you can start using vSTING. to this end:

- open the following URL in the browser: `http://kn-adrz-vsting.local`. The vSTING  user interface should be visible.

The **installation** of your vSTING device is now **completed**.

**NB**: *When using the vSTING to induce latency, a destination IP must be provided to measure the round trip time towards that destination. The perform these measurements, the vSTING needs an IP address as well. In case you are using vSTING  in a network without automatic assignment of IP adresses (i.e DHCP), you must further configure the vSTING to assign it an address in the valid network range. How to do this is explained in the usage section.*

### 3.2 Installation on custom device

It is possible to install the vSTING software on another device, such as a personal computer. However the requirement of 2 network ports must be met. USB to Ethernet Adapter can be used to provide an additional network port, as personal computers usually have only one network port.

The materials required for installing vSTING on a personal computer are as follows:

- one personal computer with at least one ethernet port
- eventually, one USB to ethernet adapter, in case the personal computer features only one ethernet port.

![Required materials for the PC installation](figs/materials-pc-install.png){width=70%}


The steps to install vSTING on your personal computer are as follows:
- install packages required for the installation process:

        sudo apt install -y coreutils sed wget git python3 iptables-persistent network-manager

- install docker and docker-compose by following this [tutorial](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). If you already have docker installed you can skip this step, but make sure the version requirements specified below are met.

  **NB**: *Don't forget to add your user to the docker group with following command*

        sudo usermod -aG docker $USER

  *Make sure you have at least docker-compose `v1.25.5` installed and that the docker-compose executable can be reached at `/usr/local/bin/docker-compose`.
  If your docker-compose is located else where you can simply add a symbolic link at the expected location as follows:*

        sudo ln -s <docker-compose_executable_path> /usr/local/bin/docker-compose

- clone the vsting repository:

        git clone https://github.com/tudo-cni/vsting-sa.git

- enter the scripts folder found in the cloned folder, make the scripts executable and download the vsting release by running the download script:

        (cd vsting-sa/scripts && chmod +x *.sh && ./download-release.sh)

- enter the release folder and configure it for your machine by running the configure script. For the configuration of vSTING, you need to specify the two network interfaces which are going to connect the robot and the operator. The configuration will create a network bridge to bind the two available network interfaces together and add the interface names in the configuration files of the vSTING submodules. Therefore, the names of the network interfaces must be provided as arguments to the configuration script like in the example below. Be sure to place the network interface connected to the robot first, and the one connected to the operator second.

        (cd vsting-sa/scripts && ./setup-custom-device.sh enp4s0 enp3s0)

- install the release on your system by running the install script:

        (cd ~/vsting && ./install.sh)

- vSTING can now be started with the following command:

        (cd ~/vsting && ./vsting.sh start)
        
  Once it is started you should be able to see the user interface by opening the following URL in your browser: `http://localhost`.
  This start is only needed after a fresh installation. the vSTING services will automatically run on computer start.


## 4. Updates

To update vsting to the latest, version run the `update.sh` script found in the scripts folder. The script checks for available newer versions, stops the current version, then proceeds to download and install the latest version. If the vsting services do not startup correctly after the update, the update is rolled back and the previous version is installed back.  
The required password is: `robocupvstingkey`

## 5. Usage

The user interface of vSTING offers a control and monitoring section. In the control section, the network constraints can be defined, enabled and disabled. The monitoring section presents the user with live network metrics the ascertain the effect of the network constratins.

### 5.1 Control Section
The control section has two variants between which the user can switch freely by clicking on the settings button at the right of the title of the control section. The two variants of the control section will now be presented in more detail.

#### 5.1.1 Simple Controls
The first variant of the control section, named `simple controls`, provides a simplified way of enabling and disabling network constraints. In this variant, predefined network constraint modes are presented to the user:

- Latency: creates 100 ms additional latency on the network link  
- Datarate: caps the maximal available transfer datarate to 10 MB  
- Packet Loss: induces 10% packet loss  
- Combined: combines all of the above.  

The user can then activate a constraint mode by clicking on it and disable it by either selecting another constraint mode, or by clikcing on the `Remove Constraints` button.

![vSTING simple controls](figs/simple-controls.PNG)

#### 5.1.2 Expert Controls

The `expert controls` is the second variant of the control section. It offers more control over the strength of the network degradation. Furthermore, the network constraints can be applied either symmetrically (same degradation from and to the robot) or asymmetrically (data packets sent to the robot experience difference degradation than packets sent from the robot).

![vSTING expert controls](figs/expert-controls.PNG)

### 5.2 Monitoring Section

The monitoring section provides insight over the following performance indicators:

- Incoming traffic: t.b.d.  
- Outgoing traffic: t.b.d.  
- Round trip time (RTT): t.b.d.  
- Packet loss: t.b.d.  

![vSTING metrics monitoring](figs/monitoring.PNG)

### 5.3 IP-Address Settings for traffic measurements

t.b.d.

#### 5.3.1 Set Destination IP

t.b.d.

#### 5.3.2 Set Source IP (if no DHCP is avaiable)

t.b.d.


## 6. Appendix

### 6.1 Set a static IP address on your device

![Set IP Address - Step 1](figs/ipset-step-1.png)

![Set IP Address - Step 2](figs/ipset-step-2.png)

![Set IP Address - Step 3](figs/ipset-step-3.png)

![Set IP Address - Step 4](figs/ipset-step-4.png)
