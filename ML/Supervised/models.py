from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Sklearn must be version 0.23.2 in stead of 0.24.2, otherwise it takes ages

models = {
    # "GNB": {"clf": GaussianNB(),
    #         "param": {"priors": [None]}
    #         }
    # ,
    "DT": {"clf": DecisionTreeClassifier(),
           "param": {"criterion": ["gini"],
                     "splitter": ["best"],
                     "class_weight": [None],
                     "max_features": ["auto"],
                     "random_state": [0]}
           }
    # ,
    # "RF": {"clf": RandomForestClassifier(),
    #        "param": {"criterion": ["gini"],
    #                  "class_weight": [None],
    #                  "max_features": ["auto"],
    #                  "n_estimators": [5, 10, 100],
    #                  "n_jobs": [-1],
    #                  "random_state": [0]}
    #        }
    # ,
    # "KNN": {"clf": KNeighborsClassifier(),
    #         "param": {"n_neighbors": [1],
    #                   "weights": ["uniform"],
    #                   # "algorithm":["ball_tree", "kd_tree"],
    #                   "n_jobs": [-1]}
    #         }
    # ,
    # "ADA": {"clf": AdaBoostClassifier(base_estimator=DecisionTreeClassifier()),
    #         "param": {"n_estimators": [10],
    #                   "random_state": [0]}
    #         }
    }
