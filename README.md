# NIDS

This github contains the code of the article ``Detecting Novel Variants of Application Layer (D)DoS Attacks using Supervised Learning" by Van de Bijl et al. 2022.

The workflow starts in the Zeek folder with the extraction of log files by Zeek. 
After extracting from the raw pcap files, other datasets can be created using the files in the other folder in Zeek.

Workflow:
1) Preprocessing with main.py
2) Sampling (D)DoS attacks and Benign 
3) Combine Layers (HTTP- TCP)
4) Train-Test Split with different splits
5) Go to ML -> Transfer -> experimental_setup.py to gather results
6) Analyze results with the interpretation folder

