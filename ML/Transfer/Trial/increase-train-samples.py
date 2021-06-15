from random import shuffle
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from BRO.utils import read_preprocessed, format_ML

def generate_figure(sizes, scores, title, output_path=None):
    plt.figure()
    plt.scatter(sizes, scores)
    plt.ylabel("F1 - Score")
    plt.xlabel("Number of malicious samples used.")
    plt.title(title)
    if output_path == None:
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(output_path + title + ".png")

def progress_learning_attack(experiment, version, protocol):
    """
    In this function, we select normal traffic and 1 attack class. We are
    interested in determining how many maliciou samples are required for
    a certain f1-score. By increasing with 10 samples, we can see the progress
    of the f1 score for a decision tree classifier.
    """

    path = get_data_folder(experiment, "BRO", version) + protocol + ".csv"
    df = read_preprocessed(path)
    output_folder = get_results_folder(experiment, "BRO", version, "Transfer Learning")

    for attack in df["Label"].unique():
        if attack != "Benign":
            df_ = df[df["Label"].isin(["Benign", attack])]

            X, y, _, _ = format_ML(df_, True)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,
                                                                random_state=1)

            index_positive = [index for index, c in enumerate(y_train) if c == 1]
            index_negative = [index for index, c in enumerate(y_train) if c == 0]

            clf = DecisionTreeClassifier()

            shuffle(index_positive)

            sample_sizes = [s*10 for s in range(1, 50) if s*10 < df[df["Label"] == attack].shape[0]]

            scores = []
            sizes = []
            for size in sample_sizes:
                select_instances = index_negative + index_positive[:size]

                clf.fit(X_train[select_instances], y_train[select_instances])
                y_pred = clf.predict(X_test)
                f1 = f1_score(y_test, y_pred)

                sizes.append(size)
                scores.append(f1)
                generate_figure(sizes, scores, protocol + "-" + attack)
            output_path_ = go_or_create_folder(output_folder, protocol)
            generate_figure(sizes, scores, protocol + "-" + attack, output_path_)

progress_learning_attack("UNSW-NB15", "2_Preprocessed", "http")