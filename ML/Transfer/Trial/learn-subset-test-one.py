"""
In this module, we seperate one attack from the others and try to learning this
attack by learning first the other attacks.
"""
import pandas as pd

from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from itertools import chain, combinations

from project_paths import get_data_folder, NID_PATH
from BRO.utils import read_preprocessed, format_ML

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def attack_learning(experiment, version, protocol):

    path = get_data_folder(experiment, "BRO", version) + protocol + ".csv"
    df = read_preprocessed(path)
    
    ddos = [a for a in df["Label"].unique() if "DoS" in a]
    df = df[df["Label"].isin(ddos + ["Benign"])]
    
    results = []
    for attack in ddos:
        other_attacks = [a for a in ddos if a != attack]
        
        df_attack = df[df["Label"] == attack]
        df_normal = df[df["Label"] == "Benign"].sample(df_attack.shape[0])
        df_test = pd.concat([df_attack, df_normal], 0) 
        X_test, y_test, _, _ = format_ML(df_test, True)
        
        df_train = df[~df["uid"].isin(df_test["uid"])] #Select normal + other attacks.    

        ps = list(powerset(other_attacks))
        
        for train_case in ps:
            if len(train_case) > 0:
                df_train_subset = df_train[df_train["Label"].isin(list(train_case) + ["Benign"])]
                X_train, y_train, _, _ = format_ML(df_train_subset, True)
            
                clf = DecisionTreeClassifier()
                clf.fit(X_train, y_train)
                y_pred = clf.predict(X_test)

                f1 = f1_score(y_test, y_pred)
                cm = confusion_matrix(y_test, y_pred)

                print("Learning attacks : " + " ".join(list(train_case)))
                print(attack + ": " + str(f1))
                print(cm)
                
                results.append([train_case, attack, f1])
    return results

results = attack_learning("CIC-IDS-2017", "2_Preprocessed", "http")

df = pd.DataFrame(results, columns = ["Learning Attacks", "Test Attack", "F1"])

df.to_csv(NID_PATH + 'prem-results.csv', sep = ";", decimal = ".")


