from Methods.Evaluation.multiclass.simulation import coin_simulate_scores, shuffle_simulate_scores
from Methods.Evaluation.multiclass.micro.coin import coin_expectations_micro, coin_optimal_theta_micro
from Methods.Evaluation.multiclass.micro.shuffle import shuffle_expectations_micro, shuffle_optimal_theta_micro
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np

#Parameters
P = [4,100]
n = np.sum(P)
c = len(P)
s = 1000

opt_coin_micro   ,_  = coin_optimal_theta_micro(P,n) 
opt_shuffle_micro,_  = shuffle_optimal_theta_micro(P,n) 
print(opt_coin_micro, opt_shuffle_micro) #Must be equal

# =============================================================================
# Checking
# =============================================================================
def plotje(df, opt_micro):
    df.plot(figsize = (10,10))
    plt.axhline(opt_micro)
    plt.ylabel("Metric Score")
    plt.xlabel("Theta")
    
coin_list = []
shuffle_list = []

for i in tqdm(range(n+1)):
    theta = [i/n, (n-i)/n]
    scores = coin_simulate_scores(theta, P, n, s, average = "micro")
    E_micro = coin_expectations_micro(theta, P, n)
    coin_list.append([E_micro, np.mean(scores,1).tolist()[0]])
    
    d = [i, n-i]
    scores = shuffle_simulate_scores(d, P, n, s, average = "micro")
    E_micro = shuffle_expectations_micro(d, P, n)
    shuffle_list.append([E_micro, np.mean(scores,1).tolist()[0]])
    
df = pd.DataFrame(coin_list, columns = ["Expectation", "Simulation"])   
df.index = df.index / n
plotje(df, opt_coin_micro)

df = pd.DataFrame(shuffle_list, columns = ["Expectation", "Simulation"])   
plotje(df, opt_shuffle_micro)







