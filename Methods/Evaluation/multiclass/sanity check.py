from Methods.Evaluation.multiclass.simulation import coin_simulate_scores, shuffle_simulate_scores
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


#Parameters setting
P = [10,40]
n = np.sum(P)
s = 1000

#Settings
average = "macro"
col = ["Recall","Precision","F1"]
columns = [c + "-Model" for c in col] + [c + "-Real" for c in col]

# =============================================================================
# Coin
# =============================================================================
coin_list = []
shuffle_list = []
for i in tqdm(range(n+1)):
    
    #Coin
    theta = [i/n, (n-i)/n]
    scores_T = coin_simulate_scores(theta, P, n, s, average = average,  modelled = True)
    scores_F = coin_simulate_scores(theta, P, n, s, average = average,  modelled = False)
    coin_list.append(np.mean(scores_T,1).tolist() + np.mean(scores_F,1).tolist())

    #Shuffle
    d = [i, n-i]
    scores_T = shuffle_simulate_scores(d, P, n, s, average = average,  modelled = True)
    scores_F = shuffle_simulate_scores(d, P, n, s, average = average,  modelled = False)
    shuffle_list.append(np.mean(scores_T,1).tolist() + np.mean(scores_F,1).tolist())

# =============================================================================
# Results
# =============================================================================

def plotjes(df):
    df.plot(figsize = (10,10)) #Plot 1
    fig, axes = plt.subplots(nrows=1, ncols=3) #Plot 2
    for i,c in enumerate(col):
        df[[a for a in df.columns if c in a]].plot(figsize=(20,10), ax=axes[i])
        
df_scores = pd.DataFrame(coin_list, columns = columns)
df_scores.index = df_scores.index / n
plotjes(df_scores)

df_scores = pd.DataFrame(shuffle_list, columns = columns)
plotjes(df_scores)





