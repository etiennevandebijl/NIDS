import numpy as np
from datetime import datetime
from sklearn.model_selection import ParameterGrid, PredefinedSplit
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV

from ML.Supervised.eval import feature_importance_statistics, \
    evaluation_metrics
from Zeek.utils import format_ML

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
    
    x_train, y_train, feature_names, labels = format_ML(df_train)
    x_test, y_test, _, _ = format_ML(df_test)
    results = {}
    for model, clf in models.items():
        print(model + "-" * (10 - len(model)) + str(datetime.now()))
        
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        
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
