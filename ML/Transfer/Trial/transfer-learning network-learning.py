"""
In this module, we have tried to learn a binary classification program on one dataset
and try to perform it on a second one. 

Issues: 
    - What to do with different intrusion ratios?
    - Which models?
    - Is this even transfer learning at all? Or can we see it as transfer learning
    because we try to label a new dataset?
"""

from project_paths import get_data_folder
from BRO.utils import read_preprocessed, format_ML
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd

path1 = get_data_folder("ISCX-IDS-2012","BRO","3_Downsampled") + "tcp.csv"
path2 = get_data_folder("UNSW-NB15","BRO","2_Preprocessed") + "tcp.csv"

df_1 = read_preprocessed(path1)
df_2 = read_preprocessed(path2)

X_train, y_train, feature_names, labels = format_ML(df_2, True)
X_test, y_test, feature_names, labels   = format_ML(df_1, True)

print(np.sum(y_train) / len(y_train)) #This is an issue
print(np.sum(y_test) / len(y_test)) #

clf = RandomForestClassifier(n_estimators = 100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
pd.DataFrame(cm, index = labels, columns = labels) 

