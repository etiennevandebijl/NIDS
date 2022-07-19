from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Sklearn must be version 0.23.2 in stead of 0.24.2, otherwise it takes ages

models = {
    "GNB": {"clf": GaussianNB(),
            "param": {"priors": [None],
                      "var_smoothing":[1e-200]} 
            }
    ,
    "DT": {"clf": DecisionTreeClassifier(),
            "param": {"criterion": ["gini","entropy"],
                      "splitter": ["best", "random"],
                      "class_weight": [None, "balanced"],
                      "max_features": ["auto", None, "sqrt", "log2"],
                      "random_state": [0]}
            }
    ,
    "RF": {"clf": RandomForestClassifier(),
            "param": {"criterion": ["gini", "entropy"],
                      "class_weight": [None, "balanced"],
                      "max_features": ["auto"],
                      "n_estimators": [10, 50, 100, 250],
                      "n_jobs": [-1],
                      "random_state": [0]}
            }
    ,
    "KNN": {"clf": KNeighborsClassifier(),
            "param": {"n_neighbors": [5],
                      "weights": ["uniform"],
                      "algorithm":["ball_tree", "kd_tree"],
                      "leaf_size":[30],
                      "n_jobs": [-1]}
            }
    }
