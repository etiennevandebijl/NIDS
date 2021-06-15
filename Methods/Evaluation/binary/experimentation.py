
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from Methods.Evaluation.binary.simulation import coin_simulate_scores, shuffle_simulate_scores
from Methods.Evaluation.binary.shuffle import shuffle_expectations
from Methods.Evaluation.binary.coin import coin_expectations

P = 5
N = 100
n = P + N

columns_coin = ["Recall coin","Precision coin","F1 score coin"]
c1_coin = [c + "-exp" for c in columns_coin] 
c2_coin = [c + "-sim" for c in columns_coin]
columns_shuffle = ["Recall shuffle","Precision shuffle","F1 score shuffle"]
c1_shuffle = [c + "-exp" for c in columns_shuffle] 
c2_shuffle = [c + "-sim" for c in columns_shuffle]

# =============================================================================
# Sanity check of expectations by simulation
# =============================================================================

'''Coin '''
s = 100000
scores = []
for i in tqdm(range(1,n+1)):
    theta = i / n
    scores_coin_exp = coin_expectations(theta, P, n)   
    scores_coin_sim = coin_simulate_scores(theta, P, N, s)
    scores.append(scores_coin_exp + np.mean(scores_coin_sim,1).tolist())


df_check = pd.DataFrame(scores, columns = c1_coin + c2_coin )
df_check.index = df_check.index / n 
df_check.plot(figsize = (10,10)) #Not really clear, maybe look at difference
plt.xlabel("Theta")
plt.ylabel("Score Metric")

differences = df_check[c1_coin].values - df_check[c2_coin].values
df_check2 = pd.DataFrame(differences, columns = columns_coin)
df_check2.index = df_check2.index / n 
df_check2.plot(figsize = (10,10)) 
plt.xlabel("Theta")
plt.ylabel("Expecation minus simulation score")

'''Shuffle '''
s = 100000
scores = []
for d in tqdm(range(0,n+1)):
    scores_shuffle_exp = shuffle_expectations(d, P, n)   
    scores_shuffle_sim = shuffle_simulate_scores(d, P, N, s)
    scores.append(scores_shuffle_exp + np.mean(scores_shuffle_sim,1).tolist())

df_check = pd.DataFrame(scores, columns = c1_shuffle + c2_shuffle )
df_check[:10].plot(figsize = (10,10), marker = '.') 
plt.xlabel("d")
plt.ylabel("Score Metric")

differences = df_check[c1_shuffle].values - df_check[c2_shuffle].values
df_check2 = pd.DataFrame(differences, columns = columns_shuffle)
df_check2.plot(figsize = (10,10))

# =============================================================================
# Experiment Progress std by the number of simulations
# =============================================================================
d = 5
theta = d / N

check = []
for s in tqdm(range(1,120)): #Begin is very interesting
    check_2 = []
    for i in range(10000):
        scores_coin = coin_simulate_scores(theta, P, N, s)
        scores_shuffle = shuffle_simulate_scores(d, P, N, s)
        trial_score = np.std(scores_coin,1).tolist() + np.std(scores_shuffle,1).tolist()
        check_2.append(trial_score)
    check.append(np.mean(check_2,0))

df = pd.DataFrame(check, columns =  columns_coin + columns_shuffle)
df[[c for c in columns_coin + columns_shuffle if "F1" in c]].plot(figsize = (15,10))

# =============================================================================
# Compare Expectations
# =============================================================================

scores = []
for d in tqdm(range(n+1)):
    theta = d / n
    scores_coin = coin_expectations(theta, P, n)   
    scores_shuffle = shuffle_expectations(d, P, n)
    scores.append(scores_coin + scores_shuffle)

df = pd.DataFrame(scores, columns = columns_coin + columns_shuffle)
df.index = df.index / n
df[:0.1].plot(figsize = (10,10))
plt.xlabel("Theta and d/n" )


