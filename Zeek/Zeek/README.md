# Zeek PCAP Processing  

This README explains how to extract network traffic features from raw PCAP files using **Zeek**.  
It covers:  
- Selected datasets used in this research  
- Installing Zeek on **Linux** and **Windows (WSL2)**  
- Running Zeek for batch processing of PCAP files  

## 1. Download Datasets  

The following datasets were used in this research:  

| Dataset       | URL                                                                                                    		|  
|---------------|---------------------------------------------------------------------------------------------------------------|  
| ISCX-IDS-2012 | [Link](http://205.174.165.80/CICDataset/ISCX-IDS-2012/Dataset/)                                               |  
| CIC-IDS-2017  | [Link](http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/)                                          |  
| UNSW-NB15     | [Link](https://cloudstor.aarnet.edu.au/plus/index.php/s/2DhnLGDdEECo4ys?path=%2FUNSW-NB15%20-%20pcap%20files) |  
| CIC-IDS-2018  | [Link](https://www.unb.ca/cic/datasets/ids-2018.html)   														|

### Notes on CIC-IDS-2018  
- The dataset requires **AWS** for downloading (~500GB).  
- Some filenames contain spaces; replace them with dashes (`-`).  
- A shortcut file in `2-3-2018` should be removed.  
- PCAP files may lack the `.pcap` extension. Rename if necessary.  


## 2. Install Zeek  

Zeek is primarily designed for **UNIX-based** systems. For **Windows**, install **WSL2** with Ubuntu 20.04 LTS. 

### Windows (WSL2 Setup)  

1. Install WSL2 following [Microsoft's guide](https://docs.microsoft.com/nl-nl/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package).  
2. Ensure WSL2 is enabled (not WSL1).  


### Linux (Ubuntu 20.04 LTS)  

Update system packages:  

```shell
sudo apt-get update -y  
sudo apt-get upgrade -y  
```

Install dependencies:

```shell
sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python3 python3-dev swig zlib1g-dev -y  
```

### Install Zeek

Follow the official installation steps [guide](https://software.opensuse.org/download.html?project=security%3Azeek&package=zeek-lts) or use the following code:

```shell
$ echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list
$ curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
$ sudo apt update
$ sudo apt install zeek-lts
```

The version used in this research: Zeek 4.0.0.

### Configure Environment

Add Zeek to the system path:
```shell
$ export PATH="$PATH:/opt/zeek/bin"
$ source ~/.bashrc
```
Verify installation:
```shell
$ zeek -h
```

If Zeek is not recognized after restarting, re-run the commands.

### Additional Tools

Convert Windows-formatted files to UNIX format:

```shell
$ sudo apt-get install dos2unix
$ dos2unix <bashfile>.sh
$ dos2unix log-reduction.zeek
```

Fix broken PCAP files:

```
$ sudo apt-get install pcapfix
```

## 3. Folder Structure

Ensure your dataset and scripts follow this structure:

-📂 Intrusion-Detection-Datasets/  
 ├── 📂 CIC-IDS-2017/  
 │    ├── 📂 Captures/ (Contains PCAP files)  
 ├── 📂 CIC-IDS-2018/  
 │    ├── 📂 Captures/ (Contains PCAP files)  
 ├── 📂 UNSW-NB15/  
 │    ├── 📂 Captures/ (Contains PCAP files)  
 ├── 📂 ISCX-IDS-2012/  
 │    ├── 📂 Captures/ (Contains PCAP files)  
 ├── 📂 CustomDataset/ (Optional additional datasets)  
 │    ├── 📂 Captures/ (Contains PCAP files)  
 ├── script-zeek.sh  
 ├── disable_streams.zeek (Excludes unnecessary logs)  

## 4. Running Zeek

Modify script-zeek.sh to fit your dataset structure, then execute:

```shell
$ sudo bash script-zeek.sh
```

The script:
- Processes multiple PCAP files at once,
- Fixes corrupted PCAP files,
- Extracts log files using Zeek.
For more customization, edit disable_streams.zeek to exclude logs not required for your analysis.

## 5. Summary

- Download datasets and organize them in the correct structure.
- Install Zeek using the provided steps for Linux/Windows (WSL2).
- Run script-zeek.sh to process PCAP files efficiently.
This setup allows batch processing of network traffic data for further analysis.



