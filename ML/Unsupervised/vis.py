import numpy as np
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# =============================================================================
# Boxplot
# =============================================================================


def boxplot_scores_label(df, model, path=None):
    f = plt.figure(figsize=(15, 12))
    ax = f.add_subplot(111)
    sns.stripplot(x="Label", y=model, data=df, ax=ax, palette="Set2",
                  split=True, linewidth=1, edgecolor='gray')
    sns.boxplot(x="Label", y=model, data=df, ax=ax,
                palette="Set2", fliersize=0)

    plt.title("Comparison of Anomaly Scores per Label")
    plt.xlabel("Label")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=70)
    plt.ylabel("Anomaly Score")

    ax.set_ylim(df[model].min(), df[model].max())
    if "IForest" in model:
        ax.set_ylim(0, 1)

    plt.tight_layout()
    if path is not None:
        plt.savefig(path + "boxplot-anomaly-score-per-label.png")
    else:
        plt.show()
    plt.close()

# =============================================================================
# Interpret df_score
# =============================================================================


def interpret_scores(df_scores, n, P, model="", output_path=None):
    values = [2 * P / (n + P),
              P / n,
              df_scores.loc[P, "F1_score"],
              df_scores["F1_score"].max(),
              df_scores["Recall"].idxmax() / n]
    df_scores.index = df_scores.index / n
    df_scores.plot(figsize=(10, 8))

    plt.axhline(y=values[0], color='black', linestyle='--')
    plt.axvline(x=values[1], color='purple', linestyle='--')
    plt.axhline(y=values[3], color='turquoise', linestyle='--')
    plt.axvline(x=values[4], color='red', linestyle='--')

    val = [str(round(v*100, 1)) + "%" for v in values]

    # Legend
    cols = df_scores.columns.tolist() + ["Baseline: " + val[0],
                                         "Anomaly Ratio: " + val[1] +
                                         " F1 Score: " + val[2],
                                         "Max F1 Score: " + val[3],
                                         "Argmax Recall: " + val[4]]
    plt.legend(cols)
    plt.title(model.split("_")[0] + " Score per Threshold Level")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("Threshold Level")
    plt.ylabel("Metric Score")

    plt.tight_layout()
    if output_path is not None:
        plt.savefig(output_path + "scores-per-threshold.png")
    else:
        plt.show()
    plt.close()

# =============================================================================
# Anomaly scores over time
# =============================================================================


def scatter_plot_ts_scores(df, model, path=None, date=None):
    median_attack = df[df["Label"] != "Benign"][model].median()
    q05_attack = df[df["Label"] != "Benign"][model].quantile(0.05)

    median_benign = df[df["Label"] == "Benign"][model].median()
    q95_benign = df[df["Label"] == "Benign"][model].quantile(0.95)

    y_max = max([median_attack, q05_attack, median_benign, q95_benign])

    labels = df["Label"].unique().tolist()
    df["Benign"] = np.where(df["Label"] == "Benign", True, False)

    colors = sns.color_palette("Paired", len(labels))
    color_dict = dict()
    for i, elem in enumerate(labels):
        color_dict[elem] = colors[i]
    color_dict["Benign"] = (0.9, 0.9, 0.9)

    f = plt.figure(figsize=(15, 7))
    ax = f.add_subplot(111)

    sns.scatterplot(y=model, x="ts", hue="Label",
                    data=df[df["Label"] == "Benign"], ax=ax,
                    palette=color_dict, s=15)
    sns.scatterplot(y=model, x="ts", hue="Label",
                    data=df[df["Label"] != "Benign"], ax=ax,
                    palette=color_dict, s=40)

    if "IForest" in model:
        y_min = 0
        y_max = 1
    else:
        y_min = df[model].min()
        y_max = max(y_max * 1.05, y_max / 1.05)
    ax.set_ylim(y_min, y_max)

    ax.set_xlim(min(df["ts"].dt.floor("H")), max(df["ts"].dt.ceil("H")))

    texts = ["MEDIAN MALICIOUS", "MEDIAN BENIGN", "95th PERCENTILE BENIGN",
             "5th PERCENTILE MALICIOUS"]
    y_values = [median_attack,  median_benign, q95_benign, q05_attack]
    x_pos = [0.878, 0.005, 0.11, 0.70]
    colors = ["red", "blue", "blue", "red"]

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)
    for i in range(len(texts)):
        if (y_values[i] < y_max and y_values[i] > y_min):
            plt.axhline(y_values[i], color=colors[i])
            pos = (y_values[i] - y_min) / (y_max - y_min)
            ax.text(x_pos[i], pos-0.01, texts[i], transform=ax.transAxes,
                    fontsize=10, bbox=props)

    handles, labels = ax.get_legend_handles_labels()
    if len(handles) > 2:
        del handles[2]
        del labels[2]
    ax.legend(handles=handles, labels=labels, loc='center left',
              bbox_to_anchor=(1, 0.5))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.xlabel("Time")
    plt.ylabel("Anomaly Score")
    plt.title("Anomaly Scores over Time per Label " + str(date.day) + " " +
              str(date.strftime("%B") + " " + str(date.year)))

    plt.tight_layout()
    if path is not None:
        plt.savefig(path + "anomaly-scores-over-time-" + str(date) + ".png")
    else:
        plt.show()
    plt.close()

# =============================================================================
# Percentages
# =============================================================================


def score_per_class(pvt, class_dist, n, path=None, threshold=""):
    g = pvt.plot(kind='bar', stacked=True,
                 figsize=(min(pvt.shape[0]*3, 15), 9), width=0.85)

    i = 0
    for index, row in pvt.iterrows():
        perc_m = row["Predicted Malicious"]
        perc_b = row["Predicted Benign"]
        if perc_b > 5:
            g.text(i,  perc_b / 2, str(round(perc_b, 1))+'%',
                   color='white', ha="center")
        if perc_m > 5:
            g.text(i, perc_b + perc_m / 2, str(round(perc_m, 1)) + '%',
                   color='white', ha="center")
        perc_total = int(class_dist.to_dict()[index] * n / 100)
        g.text(i, 103.5, "n: "+'{:,}'.format(perc_total),
               color='black', ha="center")
        g.text(i, 101, str(round(perc_total * 100 / n, 2)) + "%",
               color='black', ha="center")
        i = i + 1

    plt.axhline(100, color="black")
    g.set_xticklabels(g.get_xticklabels(), rotation=60)

    plt.ylim(0, 106)
    plt.ylabel("Percentage of Total Observations")
    plt.title("Prediction Accuracy per Label using Threshold Level " +
              threshold, fontsize=10)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    if path is not None:
        plt.savefig(path + threshold + "-malicious-labelled-per-label.png")
    else:
        plt.show()
    plt.close()

# =============================================================================
# Example
# =============================================================================
# from project_paths import get_data_folder
# from BRO.utils import read_preprocessed
# from ML.Unsupervised.utils import calculate_stats
# from BRO.learning_utils import format_ML
# from ML.Unsupervised.eval import score_statistics
# input_path  = get_data_folder("UNSW-NB15", "BRO", "3_Connection") +
#   "ftp_usl.csv"
# df = read_preprocessed(input_path)

# df = df[df["ts"].dt.date==df["ts"].dt.date.max()]
# df["score"] = np.random.uniform(0,1,size = df.shape[0])

# _scatter_plot_ts_scores(df, None, df["ts"].dt.date.min())
# stats = calculate_stats(df)
# X, y,_,_ = format_ML(df, False)
# y_pred = np.random.uniform(0,1,size = df.shape[0])
# df_scores = score_statistics(y, y_pred)

# df_scores
# df_scores.drop_duplicates(subset='Recall', keep="first")

# df_scores.index = df_scores["Recall"]
# df_scores["Precision"].plot(figsize = (10,10))

# df_scores()
# _boxplot_scores_label(df, stats, path = None)

# df["Prediction"] = np.where(df["score"] > 0.5, 1, 0)
# df["Predicted"] = np.where(df["Prediction"] == 1,
#   "Predicted Malicious","Predicted Benign")
# pvt = pd.pivot_table(df, index = "Label", columns = "Predicted",
# values = "Prediction", aggfunc = "count").fillna(0)
# pvt = (pvt.T / pvt.sum(1)).T * 100
# pvt = pvt.sort_index()
# score_per_class(pvt, stats)
