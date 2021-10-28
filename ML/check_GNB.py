
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed
from Zeek.utils import format_ML
import pandas as pd
import numpy as np

path = get_data_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS") + "Train-Test 0/http-tcp_train.csv"
data = read_preprocessed(path)

mean_label = {}
for clss, group in data.groupby("Label"):
     x_train, y_train, feature_names, labels = format_ML(group)
     mean = np.mean(x_train, axis = 0)
     std = np.std(x_train.astype(float), 0)
     mean_label[clss] = std
     
df_ = pd.DataFrame(mean_label).T
df_.columns = feature_names
