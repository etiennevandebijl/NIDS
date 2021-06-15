from scipy.stats import binom, hypergeom
import pandas as pd

n = 100
p = 0.3
P = n * p

pmfs = []
for k in range(101):
    i = binom.pmf(k, n, p)
    j = hypergeom.pmf(k, n, P, P)
    pmfs.append([i,j])
    
df = pd.DataFrame(pmfs, columns = ["Binomial","Hypergeometric"])
df.plot()



def function_1(theta, P, n):
    return (P/n) * (1-(1-theta)**n)

def function_2(theta, P, n):
    sums = 0
    for z in range(1,n+1):
        for x in range(min(z,P)+1):
            bins = binom.pmf(z, n, theta)
            hyper = hypergeom.pmf(x, n, P, z)
            sums = sums + x / z * bins * hyper 
    return sums

def function_3(theta, P, n):
    sums = 0
    for z in range(1,n+1):
        bins = binom.pmf(z, n, theta) / z
        sums2 = 0
        for x in range(min(z,P)+1):
            hyper = hypergeom.pmf(x, n, P, z) 
            sums2 = sums2 + x * hyper
        sums = sums + bins * sums2
    return sums

def function_4(theta, P, n):
    sums = 0
    for z in range(1,n+1):
        bins = binom.pmf(z, n, theta) / z
        sums2 = 0
        for x in range(min(z,P)+1):
            hyper = hypergeom.pmf(x, n-1, P-1, z-1) 
            sums2 = sums2 + (z * P / n) * hyper
        sums = sums + bins * sums2
    return sums

def function_5(theta, P, n):
    sums = 0
    for z in range(1,n+1):
        bins = binom.pmf(z, n, theta)
        sums2 = 0
        for x in range(min(z,P)+1):
            hyper = hypergeom.pmf(x, n-1, P-1, z-1) 
            sums2 = sums2 + hyper
        sums = sums + bins * sums2
    return sums * P / n


P = 1
N = 1000
n = P + N

comp = []
for i in range(100):
    theta = i / 100
    j = function_1(theta, P, n)
    k = function_2(theta, P, n)
    l = function_3(theta, P, n)
    m = function_4(theta, P, n)
    g = function_5(theta, P, n)
    comp.append([j,k,l,m,g])
    
pd.DataFrame(comp).plot(figsize = (10,10))