"""
In this module, we seperate one attack from the others and try to learning this
attack by learning first the other attacks.
"""
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

from project_paths import get_data_folder
from BRO.utils import read_preprocessed, format_ML

def attack_learning(experiment, version, protocol):
    path = get_data_folder(experiment, "BRO", version) + protocol + ".csv"
    df = read_preprocessed(path)
    for label in df["Label"].unique():
        if label != "Benign":

            #Select an attack and and euqal number of random benign instances
            df_label = df[df["Label"] == label]
            df_normal = df[df["Label"] == "Benign"].sample(df_label.shape[0])

            df_target = pd.concat([df_label, df_normal], 0)
            df_source = df[~df["uid"].isin(df_target["uid"])]

            X_train, y_train, _, _ = format_ML(df_source, True)
            X_test, y_test, _, _ = format_ML(df_target, True)

            clf = DecisionTreeClassifier()
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)

            f1 = f1_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)

            print(label + ": " + f1)
            print(cm)

attack_learning("CIC-IDS-2017", "2_Preprocessed", "tcp")
