# Zeek read PCAPS

In this readme, I will show how raw network traffic (PCAP) is extracted by Zeek. 
First, I will show which datasets were selected for this research. Afterwards, I will show 
how Zeek can be applied on a Linux and a Windows machine. As I don't have experience with 
MAC and don't have one, this OS will not be included as I don't know which steps are required.
Still, approximately the same steps can be applied for MAC, so it might be later added. 

## Download datasets

I considered the following four datasets usefull for now. ISCX-IDS-2012, CIC-IDS-2017
UNSW-NB15 and the CIC-IDS-2018.

| Dataset  | URL | 
| ISCX-IDS-2012 | http://205.174.165.80/CICDataset/ISCX-IDS-2012/Dataset/ |
| CIC-IDS-2017 | http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/ |
| UNSW-NB15 | https://cloudstor.aarnet.edu.au/plus/index.php/s/2DhnLGDdEECo4ys?path=%2FUNSW-NB15%20-%20pcap%20files |
| CIC-IDS-2018 | https://www.unb.ca/cic/datasets/ids-2018.html |

For the first three datasets the pcaps can simply be downloaded (with wget or something).
You can also do it manually. Note that in the CIC-IDS-2018 there are some remarks:
- You have to use AWS to gather the data. It takes a lot of time as it is alomst 500 GB.
- Some files have spaces in their name: replace those spaces with a dash ("-").
- There is a shortcut in 2-3-2018. You must remove this one.
- The files do not have a .pcap format. This could cause a problem but not necessarily. 

## Install ZEEK

Now I will describe how ZEEK can be installed and which version I used to do this. 
As Zeek uses UNIX (I guess), you will have to install Ubuntu 20.04 LTS for Windows 10.
I guess it is only possible to get this working for some window 10 versions, so check that just
in case. 

### Windows
To install ubuntu (or another linux distro) using WSL2 (note that your must use WSL2 and not WSL1), you need to follow
the following instructions to install it. 
https://docs.microsoft.com/nl-nl/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package


### Linux / UBUNTU LTS

Let us first get the latest updates/upgrades.

```shell
$ sudo apt-get update -y
$ sudo apt-get upgrade -y
```

Install dependencies of Zeek (or check the website https://docs.zeek.org/en/current/install.html).

```shell
$ sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python3 python3-dev swig zlib1g-dev -y
```

Install zeek (https://software.opensuse.org/download.html?project=security%3Azeek&package=zeek-lts) do steps in this order and all of them.
You can also follow the steps given in the link.

```shell
$ echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
$ curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
$ sudo apt update
$ sudo apt install zeek-lts
```

The Zeek version I used was version 4.0.0. I didn't want to configure mail. Zeek won't work before adding zeek to the PATH environment variable:
```shell
$ export PATH="$PATH:/opt/zeek/bin"
$ source ~/.bashrc
```
To test is Zeek works, use the following command:
```shell
$ zeek -h
```

It might happen that these steps are not permanent. Therefore you can see that zeek does not work when you command zeek. Therefore, reuse these steps to get it working.

For the Windows users, it might happen that some files are not unix. Therefore you can use a package called dos2unix to convert files to unix.

```shell
$ sudo apt-get install dos2unix
$ dos2unix <bashfile>.sh
$ dos2unix log-reduction.zeek
```

We need also a packet fixer when packets are broken, you can turn this on or off in the script.bash

```
$ sudo apt-get install pcapfix
```

To make the zeek script work as I did in my research, you should have the following structure in your folders:

- disable_streams.zeek (zeek script to turn off streams) 
- script-zeek.sh
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
	- Your own folder of some dataset/experiment (extra)
		- Captures/
			- Here are (subfolders containing) only pcap files.

You can adjust the script-zeek file to make the bash program work to your own preference. 
To get the bash file working, cd with ubuntu to the script-zeek.sh file and start the bash file using:

```shell
$ sudo bash script-zeek.sh
```

Note that the disable_streams.zeek file is a zeek script to exclude streams log files we (I) do not necessarily need in (my) research. 
With the bash script we can process multiple files at ones, fix the pcaps and scope the log files in one go. 
You can do it manually, but with this script it saves a lot of time. 

