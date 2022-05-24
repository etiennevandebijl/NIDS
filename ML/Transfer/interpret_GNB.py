from project_paths import get_data_folder
from Zeek.utils import read_preprocessed
from Zeek.utils import format_ML
from sklearn.naive_bayes import GaussianNB
import pandas as pd


data_path = get_data_folder("CIC-IDS-2018", "BRO", "2_Preprocessed_DDoS") + "Train-Test 1/"
file_path = data_path + "http-tcp_train.csv"
df_train = read_preprocessed(file_path)
df_test = read_preprocessed(file_path.replace("_train", "_test"))


df_train = df_train[df_train["Label"].isin(["DoS - GoldenEye", "DoS - Slowloris", "Benign"])]
df_train.loc[df_train["Label"].isin(["DoS - GoldenEye", "DoS - Slowloris"]), 'Label'] = "Malicious"

df_test = df_test[df_test["Label"].isin(["DoS - Hulk", "Benign"])]
df_test.loc[df_test["Label"].isin(["DoS - Hulk"]), 'Label'] = "Malicious"

x_train, y_train, feature_names, labels = format_ML(df_train)
x_test, y_test, _, _ = format_ML(df_test)

clf = GaussianNB(var_smoothing=1e-200)

clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
y_pred_proba = clf.predict_log_proba(x_test)

preds = pd.DataFrame(y_pred_proba)
preds["Label"] = y_test
preds["Prediction"] = y_pred

preds = preds[preds["Label"] != preds["Prediction"]]
