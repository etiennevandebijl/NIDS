# Raw Pcap to json log files with Zeek

First download the following pcaps using the following URLS:
ISCX-IDS-2012: http://205.174.165.80/CICDataset/ISCX-IDS-2012/Dataset/
CIC-IDS-2017: http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/
CIC-IDS-2018: https://www.unb.ca/cic/datasets/ids-2018.html
UNSW-NB15: https://cloudstor.aarnet.edu.au/plus/index.php/s/2DhnLGDdEECo4ys?path=%2FUNSW-NB15%20-%20pcap%20files

Note that in the CIC-IDS-2018 there are some issues:
- You have to use AWS to gather the data. It takes a lot of time as it is alomst 500 GB.
- Some files have spaces in their name: replace those spaces with a dash ("-").
- There is a shortcut in 2-3-2018. You must remove this one.
- The files do not have a .pcap format. This could cause a problem but not necessarily. 

## Windows
Steps to get Zeek working on a ubuntu LTS in a Windows 10 machine. 

0.1) Install ubuntu 20.04 LTS
When using Windows, a workaround can be used to get a linux system required for running ZEEK.
First, we need to perform the following steps in order to install ubuntu on our Windows machine:
https://docs.microsoft.com/nl-nl/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package

## Linux / UBUNTU LTS

Install Zeek
Perform the following steps of code:

```shell
$ sudo apt-get update -y
$ sudo apt-get upgrade -y
```

Install dependencies of Zeek (or check the website https://docs.zeek.org/en/current/install.html)
```shell
$ sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python3 python3-dev swig zlib1g-dev -y
```

Install zeek (https://software.opensuse.org/download.html?project=security%3Azeek&package=zeek-lts) do steps in this order and all of them.

```shell
$ echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
$ curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
$ sudo apt update
$ sudo apt install zeek-lts
```

Zeek won't work before adding zeek to the PATH environment variable:
```shell
$ export PATH="$PATH:/opt/zeek/bin"
$ source ~/.bashrc
```
It might happen that these steps are not permanent. Therefore you can see that zeek does not work when you command zeek. Therefore, reuse these steps to get it working.

To make bash files work (could happen it breaks) install dos2unix
```shell
$ sudo apt-get install dos2unix
$ dos2unix <bashfile>.sh
$ dos2unix log-reduction.zeek
```

We need also a packet fixer when packets are broken, you can turn this on or off in the script.bash

We also need a package to fix the pcaps if packets are broken
```
$ sudo apt-get install pcapfix
```

To make the zeek script work as I did in my research, you should have the following structure in your folders:

- log-reduction.zeek 
- script-zeek-new.sh
- Intrusion-Detection-Datasets/
	- CIC-IDS-2017/
		- Captures/
			- Here are (subfolders containing) only pcap files
	- CIC-IDS-2018/
		- Captures/
		 	- Here are (subfolders containing) only pcap files
	- UNSW-NB15/
		- Captures/
		 	- Here are (subfolders containing) only pcap files
	- ISCX-IDS-2012/
		- Captures/
		 	- Here are (subfolders containing) only pcap files
	- Your own folder of some dataset/experiment
		- Captures/
			- Here are (subfolders containing) only pcap files.


You can adjust the script-zeek-new file to make the bash program work to your own preference. 
To get the bash file working, cd with ubuntu to the script-zeek-new.sh file and start the bash file using:

```shell
$ bash script-zeek-new.sh
```

Note that the log-reduction.zeek file is a zeek script to exclude log files we (I) do not necessarily need in (my) research. With the bash script we can process multiple files at ones,
fix the pcaps and scope the log files in one go. You can do it manually, but with this script it saves a lot of time. 