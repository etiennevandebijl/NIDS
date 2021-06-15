"""
In this module we use a certain dataset from the set of datasets and try to perform
a version of transfer learning. To be more specific, we only select DDoS/DoS attacks
as the interest was more focussed on these kind of attacks. We use for both the train
and test dataset all benign traffic but use only one attack to train on and one to
test on. We also perform some hyperparameter tuning in a randomized manner.
"""

#Author: Etienne van de Bijl 2020

from sklearn.model_selection import ParameterSampler
from sklearn.metrics import f1_score

from project_paths import get_data_folder
from BRO.utils import read_preprocessed, format_ML
from ML.Supervised.models import models

def hyper_parameter_tuning(df_train, df_test):
    """
    This function searches the parameter space of different models to find
    the best parameters (highest f1 score) and returns a dictionary with the
    model with the best f1 scores.

    """
    X_train, y_train, _, _ = format_ML(df_train, True)
    X_test, y_test, _, _ = format_ML(df_test, True)

    performance_dict = {}
    for model, settings in models.items():
        clf = settings["clf"]
        highest_f1_score = 0.0
        for params in list(ParameterSampler(settings["param"], n_iter=10, random_state=0)):
            clf.set_params(**params)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            score = f1_score(y_test, y_pred)

            if score >= highest_f1_score:
                highest_f1_score = score
        performance_dict[model] = highest_f1_score
    return performance_dict

def transfer_learning_idea(experiment, version, protocol):
    path = get_data_folder(experiment, "BRO", version) + protocol + ".csv"
    df = read_preprocessed(path)

    ddos = [a for a in df["Label"].unique() if ("DoS" in a or "DDoS" in a or "Bot" in a)]
    df = df[df["Label"].isin(ddos + ["Benign"])]

    scores_test = []
    for train_attack in ddos:
        df_train = df[df["Label"].isin(["Benign", train_attack])]
        for test_attack in ddos:
            print(train_attack + " " + test_attack)
            df_test = df[df["Label"].isin(["Benign", test_attack])]

            performance_dict = hyper_parameter_tuning(df_train, df_test)
            scores_test.append([train_attack, test_attack, performance_dict])
    return scores_test

SCORES = transfer_learning_idea("CIC-IDS-2017", "2_Preprocessed", "http")
