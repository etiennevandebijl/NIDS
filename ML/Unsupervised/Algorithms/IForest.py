import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyod.models.iforest import IForest
import seaborn as sns
from sklearn.model_selection import KFold
from pyod.models.pca import PCA

rng = np.random.RandomState(42)

# Generating training data 
D_normal = 0.5 * rng.randn(10000, 2)
D_normal = np.r_[D_normal + 3, D_normal]
D_normal = pd.DataFrame(D_normal, columns = ['x1', 'x2'])
D_normal["Label"] = "Benign"
D_normal.shape

# Generating outliers
circle = 1.65

D_outliers = []
while len(D_outliers) < 50:
    outlier = rng.uniform(low=-2.5, high=5.5, size=(2))
    if outlier[0] > -1.65 and outlier[0] < 1.65 and outlier[1] > -1.65 and outlier[1] < 1.65:
        continue
    elif outlier[0] > 3 - circle  and outlier[0] < 3 + circle and outlier[1] > 3 - circle and outlier[1] < 3 + circle:
        continue
    D_outliers.append(outlier)

D_outliers = pd.DataFrame(D_outliers, columns = ['x1', 'x2'])
D_outliers["Label"] = "Outlier"

D = pd.concat([D_normal,D_outliers])
print(D.shape)
plt.figure(figsize = (10,10))
sns.scatterplot(x = "x1", y = "x2", hue = "Label", data = D)

X = D.drop(["Label"],1).values
y = D["Label"].values

clf = PCA()

K = 10
kf = KFold(n_splits=10, shuffle=True, random_state = 1)

y_pred_all    = np.zeros(X.shape[0])    
y_pred_benign = np.zeros(X.shape[0])

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
        
    clf.fit(X_train)
    y_pred_all[test_index] = [s + 0.5 for s in clf.decision_function(X_test)]
        
    benign_index = [i for i, x in enumerate(y[train_index]) if x == "Benign"]
    clf.fit(X_train[benign_index])           
    y_pred_benign[test_index] = [s + 0.5 for s in clf.decision_function(X_test)]
        
D_ = D.copy()
D_["Train on ALL"] = y_pred_all
D_["Train on BENIGN"] = y_pred_benign

#plt.figure(figsize = (10,10))
#sns.scatterplot(x = "AS1", y = "AS2", hue = "Label",data = D_)         
plt.figure(figsize = (10,10))
sns.catplot(x = "Label", y = "Train on ALL", data = D_)

print(D_.groupby("Label")["Train on ALL","Train on BENIGN"].agg("mean"))
print(D_.groupby("Label")["Train on ALL","Train on BENIGN"].agg("std"))



























