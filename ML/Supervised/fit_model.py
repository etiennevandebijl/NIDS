import numpy as np
from datetime import datetime
from sklearn.model_selection import ParameterGrid, PredefinedSplit
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV

from ML.Supervised.eval import feature_importance_statistics, \
    evaluation_metrics
from Zeek.utils import format_ML


# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# from sklearn.metrics import f1_score

def hyper_parameter_tuning(X, y, labels, splitter, settings):
    if len(list(ParameterGrid(settings["param"]))) == 1:
        clf = settings["clf"]
        new_dict = {}
        for key, value in settings["param"].items():
            new_dict[key] = value[0]
        clf.set_params(**new_dict)
        return clf

    scorer = "f1_weighted"

    if ("Benign" in labels) and (len(labels) == 2):
        other_labels = [la for la in labels if la != 'Benign']
        scorer = make_scorer(f1_score, pos_label=other_labels[0])

    clf = GridSearchCV(settings["clf"], settings["param"], scoring=scorer,
                       cv=splitter, n_jobs=-1)
    clf.fit(X, y)
    return clf.best_estimator_


def apply_splitter(X, y, clf, splitter):
    fitted_models = []
    predicted_indices = []
    y_pred = np.array([None] * X.shape[0])

    for train_index, test_index in splitter.split(X, y):
        clf.fit(X[train_index], y[train_index])
        y_pred[test_index] = clf.predict(X[test_index])
        fitted_models.append(clf)
        predicted_indices.extend(test_index)
    return y_pred, fitted_models, sorted(predicted_indices)


def perform_train_validation(df, models, splitter):
    X, y, feature_names, labels = format_ML(df)

    results = {}
    for model, settings in models.items():
        print(model + "-" * (10 - len(model)) + str(datetime.now()))

        clf = hyper_parameter_tuning(X, y, labels, splitter, settings)
        y_pred, fitted_models, predicted_indices = apply_splitter(X, y, clf,
                                                                  splitter)

        df_scores = evaluation_metrics(y[predicted_indices],
                                       y_pred[predicted_indices], labels)
        df_fi = feature_importance_statistics(fitted_models,
                                              model, feature_names)
        results[model] = [clf, df_scores, df_fi]
    return results


def perform_train_test(df_train, df_test, models):
    
    ######################################################################
    ######################################################################
    ######################################################################
    
    
    # remove_features = [] #list(df_train.select_dtypes([bool]).columns)
    # for label, group in df_train.groupby("Label"):
    #     x_train, y_train, feature_names, labels = format_ML(group)
    #     X = pd.DataFrame(x_train, columns = feature_names)
    #     r_f = [c for c in X.columns if X[c].std() < 1]
    #     remove_features.extend(r_f)
    # remove_features = list(set(remove_features))
    # df_train = df_train.drop(remove_features, axis=1)
    # df_test = df_test.drop(remove_features, axis=1)    
    ######################################################################
    ######################################################################
    ######################################################################
    
    x_train, y_train, feature_names, labels = format_ML(df_train)
    x_test, y_test, _, _ = format_ML(df_test)
    #print(feature_names)
    results = {}
    for model, clf in models.items():
        print(model + "-" * (10 - len(model)) + str(datetime.now()))
        
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)

        ######################################################################
        ######################################################################
        ######################################################################
        # df_mu = pd.DataFrame(clf.sigma_, columns = feature_names)
        # df = df_mu.T
        # for label, group in df_train.groupby("Label"):
        #     x_train, _, _, _ = format_ML(group)
        #     df[label] = np.var(x_train, axis = 0)
        # #df_sigma = pd.DataFrame(clf.sigma_, columns = feature_names)
        # #df = pd.concat([df_mu, df_sigma], ignore_index=True)
        # #df = df.astype(int).T
        # #df.columns = ["mu M", "mu B", "sigma M", "sigma B"]
        # print(df.astype(int))
        
        # df = pd.DataFrame(clf.predict_proba(x_test), columns = ["Benign", "Malicious"])
        # df["Label"] = y_test
        # df["Prediction"] = clf.predict(x_test)
        
        # cm = confusion_matrix(y_test, df["Prediction"], labels=labels)
        # print("Test")
        # dd = pd.DataFrame(cm, columns = ["Predicted B", "Predicted M"])
        # dd["Total"] = cm.sum(1)
        # dd = dd.T
        # dd.columns = ["Real B", "Real M"]
        # dd["Total"] = list(cm.sum(0)) + [cm.sum()]
        # print(dd.T * 100 / cm.sum())

        
        # df = pd.DataFrame(clf.predict_proba(x_train), columns = ["Benign", "Malicious"])
        # df["Label"] = y_train
        # df["Prediction"] = clf.predict(x_train)
        
        # cm = confusion_matrix(y_train, df["Prediction"], labels=labels)
        # print("Train")
        # dd = pd.DataFrame(cm, columns = ["Predicted B", "Predicted M"])
        # dd["Total"] = cm.sum(1)
        # dd = dd.T
        # dd.columns = ["Real B", "Real M"]
        # dd["Total"] = list(cm.sum(0)) + [cm.sum()]
        # print(dd.T * 100 / cm.sum())

        # df = df.sort_values("Malicious")
        # df["Integer"] = range(df.shape[0])
        
        # fig, ax = plt.subplots(figsize=(8,6))
        # for label, group in df.groupby('Label'):
        #     group["Malicious"].plot(kind="hist", ax=ax, label=label)
        # plt.legend()
        # plt.xlim(0,1)
        # plt.show()
        
        # plt.figure(figsize=(8,6))
        # sns.boxplot(x = "Label", y = "Malicious", data = df)
        # plt.show()
        
        # for label, group in df.groupby("Label"):
        #     plt.figure(figsize = (8,6))
        #     sns.scatterplot(x = "Integer", y = "Malicious", hue = "Label", data = group)
        #     plt.show()
        ######################################################################
        ######################################################################
        ######################################################################
        
        df_scores = evaluation_metrics(y_test, y_pred, labels)
        df_fi = feature_importance_statistics([clf], model, feature_names)
        results[model] = [clf, df_scores, df_fi]
    return results


def perform_train_test_search_opt_params(df_train, df_test, models):
    df = df_train.append(df_test).reset_index(drop=True)

    test_fold = [-1] * df_train.shape[0] + [0] * df_test.shape[0]
    ps = PredefinedSplit(test_fold)

    results = perform_train_validation(df, models, ps)
    return results
