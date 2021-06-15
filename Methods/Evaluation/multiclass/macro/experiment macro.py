from Methods.Evaluation.multiclass.simulation import coin_simulate_scores, shuffle_simulate_scores
from Methods.Evaluation.multiclass.macro.coin import coin_expectations_macro, coin_optimal_macro
from Methods.Evaluation.multiclass.macro.shuffle import shuffle_expectations_macro, shuffle_optimal_macro
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np

#Parameters
P = [10,43]
n = np.sum(P)
c = len(P)
s = 10000

col = ["Recall","Precision","F1"]
columns = [c + "-Exp" for c in col] + [c + "-Sim" for c in col]    

opt_coin_macro       = coin_optimal_macro(P,n) 
opt_shuffle_macro    = shuffle_optimal_macro(P) 
print(opt_coin_macro, opt_shuffle_macro) 

# =============================================================================
# Checking
# =============================================================================
def plotje(df, opt_micro, metric):
    df.plot(figsize = (10,10))
    plt.axhline(opt_micro, color = "r")
    plt.ylabel("Metric Score")
    plt.xlabel("Theta")
    plt.title(metric)
    plt.show()
    
coin_list = []
shuffle_list = []

for i in tqdm(range(n+1)):
    theta = [i/n, (n-i)/n]
    scores = coin_simulate_scores(theta, P, n, s, average = "macro")
    E_macro = coin_expectations_macro(theta, P, n)
    coin_list.append(E_macro + np.mean(scores,1).tolist())
    
    d = [i, n-i]
    scores = shuffle_simulate_scores(d, P, n, s, average = "macro")
    E_macro = shuffle_expectations_macro(d, P, n)
    shuffle_list.append(E_macro + np.mean(scores,1).tolist())

#Coin
df = pd.DataFrame(coin_list, columns = columns)   
df.index = df.index / n
for i,c in enumerate(col):
    plotje(df[[a for a in df.columns if c in a]], opt_coin_macro[i], c)

#Shuffle
df = pd.DataFrame(shuffle_list, columns = columns)   
for i,c in enumerate(col):
    plotje(df[[a for a in df.columns if c in a]], opt_shuffle_macro[i], c)
