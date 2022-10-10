import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import squareform, pdist
from Zeek.utils import read_preprocessed, format_ML
from project_paths import get_results_folder, get_data_folder
from ML.Transfer.experimental_setup import NAMES

NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2017"
PROTOCOL = "http-FIX-tcp-FIX"
RS = 10

#%% 

results = []
feature_names = []
for rs in range(RS):
    input_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS",
                                "Supervised") + "Train-Test " + str(rs) + "/Paper/" + PROTOCOL + "/"

    for file in glob.glob(input_path + '**/feature_importance.csv', recursive=True):
        tags = file.split(os.sep)
        train_attacks = tags[-2].split(" ")
        test_attack = tags[-3]

        train_attacks = [NAMES_[l] for l in train_attacks]
        number_of_attacks = len(train_attacks)

        df = pd.read_csv(file, sep=";", decimal=",", index_col=0).fillna(0)

        for model in df:
            instance = [test_attack, len(train_attacks), str(train_attacks), rs, model]
            instance.extend(df[model].values)
            results.append(instance)
        feature_names = list(df.index)
    
col_names = ["Test", "Number of trained D(D)oS attacks",
            "Train", 'RS' , "Model"] + feature_names 
        
df = pd.DataFrame(results, columns = col_names)

#%%
MODEL = "RF"
df_ = df[df["Number of trained D(D)oS attacks"] == 1]
df_ = df_[df_["Model"] == MODEL]
df_ = df_[[x in y for x, y in df_[['Test','Train']].values]]
df_.drop(columns = ["Number of trained D(D)oS attacks", "Model", "Train"], axis = 1, inplace = True)

df_.index = df_["Test"]
df_.drop(columns = ["Test"], inplace = True)

for attack, group in df_.groupby(["Test"]):
    ignore_features = group.T[group.T.max(axis = 1) < 0.01].index
    group_ = group.drop(columns = ignore_features, axis = 1)
    
    group_ = group_.reset_index().set_index(["RS"])
    group_.drop("Test", axis = 1, inplace = True)
    group_ = group_.unstack(level = -1).reset_index()
    group_.columns = ["Feature","RS","Feature importance"]

    plt.figure(figsize = (10, 10))
    if False:
        sns.swarmplot(x = "Feature importance", y = "Feature", hue = "RS" ,data = group_ )
        plt.title("Detecting " + attack + " swarmplot with " + MODEL)
    else:
        sns.boxplot(x = "Feature importance", y = "Feature", data = group_ )
        plt.title("Detecting " + attack + " boxplot with " + MODEL)
    plt.show()


ignore_features = group.T[group.T.max(axis = 1) < 0.01].index


table = df_.groupby(["Test"]).mean().T

ignore_vars = list(table[table.max(axis = 1) < 0.05].index)


table = table.drop(table[table.max(axis = 1) < 0.05].index)
distances = squareform(pdist(table.T))
distances = pd.DataFrame(distances, columns = table.columns, index = table.columns)
plt.figure()
table.plot.barh(figsize = (20,20), title= "RF feature importance averages")
plt.show()

# %% PCA over most interesting features

table = df_.groupby(["Test"]).mean().T

ignore_vars = table[table.max(axis = 1)<0.01].index

data_path = get_data_folder(DATASET, "BRO", "2_Preprocessed_DDoS")
    
dataset = read_preprocessed(data_path + "http-FIX-tcp-FIX.csv")
dataset = dataset.drop(columns = ignore_vars, axis = 1)

X, y, _, labels = format_ML(dataset)

index_B = dataset.index[dataset['Label'] == "Benign"].tolist()
index_M = dataset.index[dataset['Label'] != "Benign"].tolist()
            
X = StandardScaler().fit(X).transform(X)
            
#Step 2 fit PCA on normal traffic and transform all data
model = PCA(n_components=3)
model.fit(X[index_B, :])
print(model.explained_variance_ratio_)
X = model.transform(X)

colors = sns.color_palette("Paired",len(labels))
color_dict = dict()
for i, elem in enumerate(labels):
    color_dict[elem] = colors[i]
color_dict["Benign"] = (0.9,0.9,0.9)
            
f = plt.figure(figsize=(15,7))
ax = f.add_subplot(111)
#sns.scatterplot(x = X[index_B,0], y = X[index_B,1], hue =y[index_B], ax=ax, palette = color_dict, s = 15)
sns.scatterplot(x = X[index_M,0], y = X[index_M,1], hue =y[index_M], ax=ax, palette = color_dict, s = 40)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.xlim(-1.5,0.2)
plt.ylim(-3,3)
plt.plot()
