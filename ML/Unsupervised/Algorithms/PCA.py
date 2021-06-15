from project_paths import get_data_folder
from BRO.utils import read_preprocessed
from BRO.learning_utils import format_ML
import matplotlib.pyplot as plt
import seaborn as sns
from pyod.models.pca import PCA
from sklearn.decomposition import PCA as PCA_sklearn
from sklearn import preprocessing
import numpy as np
from scipy.spatial.distance import cdist

input_folder = get_data_folder("CIC-IDS-2017", "BRO", "3_Connection")
df = read_preprocessed(input_folder + "tcp_usl.csv")

X, y,_,_ = format_ML(df, False)
X_scaled = preprocessing.scale(X)

for i in range(1,X.shape[1]):
    clf = PCA(n_components = i)
    benign_index = [i for i, x in enumerate(y) if not x]
    clf.fit(X_scaled[benign_index])       

    clf.fit(X_scaled)
    y_pred = np.log(clf.decision_function(X_scaled))

    sort_index = np.argsort(y_pred)
    y_pred_sort = y[sort_index]
    y_pred_sort = y_pred_sort[::-1]
    line = np.cumsum(y_pred_sort)/ np.sum(y)
    
    plt.figure(figsize = (10,10))
    plt.plot(line)
    plt.show()

# =============================================================================
# Check properties
# =============================================================================
import pandas as pd
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data

X_scaled = preprocessing.scale(X)
np.mean(X_scaled,0)
np.var(X_scaled,0)

## PYOD
clf = PCA()
clf.fit(X_scaled)
y_pred = clf.decision_function(X_scaled)

#Sklearn
clf = PCA_sklearn()

#Transform data Option 1
X_scaled_transform = clf.fit_transform(X_scaled) 

#Transform data Option 2
clf.fit(X_scaled)

#Sanity check
df_I = np.matmul(clf.components_.T, clf.components_) #This should be identity matrix

X_scaled_transform_ = np.matmul(X_scaled, clf.components_.T) #This is equal to the original thing

#Santity Check if variance is equal to eigenvalues
print(np.mean(X_scaled_transform_,0)) #0
print(np.var(X_scaled_transform_,0))
print(clf.explained_variance_)
pd.DataFrame(X_scaled_transform_).corr() #Covariances must be 0

#This is how it is calculated. But it this what we want? Is it even correct? n_selected means taking the last items
y_pred_PYOD = np.sum( cdist(X_scaled, clf.components_) / clf.explained_variance_ratio_, axis = 1).ravel()
#explained_variance_ratio_ this is important to notice as it is not the eigenvalues themself.
#Also the cdist seems not according to the paper (?) It is the euclidean distance

#I would say this would be more correct
y_pred_Etienne = np.sum( np.matmul(X_scaled, clf.components_.T)**2 / clf.explained_variance_, axis = 1).ravel()


plt.scatter(y_pred,y_pred_PYOD)
plt.scatter(y_pred,np.log(y_pred_Etienne))

plt.figure(figsize = (15,15))
sns.scatterplot(np.log(y_pred),np.log(y_pred_Etienne),hue = y)

plt.figure(figsize = (15,15))
sns.scatterplot(y_pred,np.log(y_pred_PYOD),hue = y)



y_index = [i for i,b in enumerate(y) if b]

scores = y_pred_Etienne[y_index]



plt.boxplot(np.log(y_pred_Etienne),)
plt.plot(y_pred_Etienne)

np.sum(clf.explained_variance_ratio_) #This i s 1

#Why ratio and not the eigenvalues themself
X_check = np.matmul(X_scaled, clf.components_.T)
np.var(X_check,0)

#This is interesting to do, but can do in a later stadium

def PCA_grid_search(X,clf):
    #print(clf.explained_variance_ratio_) #Sanity check
    scores_ = dict()
    for i in range(X.shape[1] + 1):
        print(i)
        for j in range(i-1,i):
            n_components = i
            n_selected_components = j + 1
            
            #PYOD
            weights = clf.explained_variance_ratio_[i-j-1:i]
            pca_components = clf.components_[i-j-1:i,:]
            #print(n_components,n_selected_components,weights) #Sanity check
            y_pred_PYOD = np.sum( cdist(X, pca_components) / weights, axis = 1).ravel()
            
            scores_[(n_components,n_selected_components)] = y_pred_PYOD
    return scores_

scores_ = PCA_grid_search(X_scaled,clf)


























