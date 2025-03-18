# NIDS  

This repository contains the code for the article **"Detecting Novel Application Layer Cybervariants Using Supervised Learning"** by van de Bijl et al. (2022).  

## Overview  

The code provides a workflow for detecting novel (D)DoS and Web attacks at the application layer using supervised learning techniques. The process starts with extracting log files from raw PCAP data using **Zeek** and continues through preprocessing, sampling, feature extraction, and machine learning experiments.  

## Workflow  

1. **Extract Log Files**  
   - Use the scripts in the `Zeek/Zeek` folder to extract logs from raw PCAP files.  

2. **Preprocessing**  
   - Run `main.py` in `Zeek\Preprocessing\` to preprocess the extracted logs.  

3. **Sampling**  
   - Sample different categories: (D)DoS attacks, web attacks, and benign traffic.  

4. **Feature Engineering**  
   - Combine different layers (e.g., HTTP and TCP) for richer feature representation.  

5. **Train-Test Split**  
   - Apply different train-test split strategies.  

6. **Model Training & Evaluation**  
   - Navigate to `ML/Transfer/experimental_setup.py` to run experiments and gather results.  

7. **Interpretation & Analysis**  
   - Use the scripts in the `interpretation` folder to analyze results.  

## Environment  

- The code is designed to run in an **Anaconda** environment.  
- Ensure all dependencies are installed before running the scripts.  

## Getting Started  

1. Clone this repository:  
   ```bash
   git clone https://github.com/etiennevandebijl/NIDS.git  
   cd NIDS  

2. Set up your Anaconda environment (if not already configured):
    ```bash
    conda env create -f environment-NIDS.yml   
    conda activate NIDS  
    ```
3. Follow the workflow steps above.

## Citation
If you use this code in your research, please cite:

E.P. van de Bijl, J.G. Klein, J. Pries, R.D. van der Mei, and S. Bhulai, **"Detecting novel application layer cybervariants using supervised learning"**, International Journal on Advances in Security, volume 15, number 3 & 4, pages 75-85, 2022.