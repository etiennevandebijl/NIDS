import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from application import Application, tk
from project_paths import get_data_folder, get_results_folder
from Zeek.utils import read_preprocessed, print_progress
from sklearn.model_selection import train_test_split
sns.set(font_scale=1.2)

RS = 4
VMAP = {-3: "Train (64%)", -2: "Validation (16%)", -1: "Test (20%)"}

def determine_cmap(dataset, vmap):
    n = len(vmap)
    cmap = []
    if -4 in dataset.values:
        cmap = [(1,1,1)]

    if -1 in dataset.values:
        cmap = cmap + [sns.color_palette("Paired")[3],
                sns.color_palette("Set2")[5],
                sns.color_palette("Paired")[5]]
        vmap =  {**VMAP, **vmap}
    if -4 in dataset.values:
        vmap =  {**{-4: "White"}, **vmap}
    cmap = cmap + [sns.color_palette("Set2")[-1]] + sns.color_palette("Blues", n - 1)
    return cmap, vmap


def set_colorbar(ax, vmap):
    colorbar = ax.collections[0].colorbar
    mini = colorbar.vmin
    if -4 in vmap.keys():
        vmap = {k:v for k,v in vmap.items() if k !=- 4}
        mini = mini + 1
    n = len(vmap)
    r = colorbar.vmax - mini
    colorbar.set_ticks([mini + 0.5 * r / (n) + r * i / (n) for i in range(n)])
    colorbar.set_ticklabels(list(vmap.values()))


def plot_heatmap(dataset, vmap, vc, cols, protocol, output_folder):
    cmap, vmap = determine_cmap(dataset, vmap)
    
    plt.figure(figsize = (20, min(8,4 * dataset.shape[1])))
    ax = sns.heatmap(dataset.T.sort_index(), cmap=cmap)
    set_colorbar(ax, vmap)
    
    for index in np.cumsum(vc):
        ax.axvline(index, color='white', lw=10)
    
    for i in range(dataset.shape[1]):
        ax.axhline(i + 1 , color='white', lw=10)

    plt.xlabel("Instance")
    plt.yticks(rotation = 0)
    plt.tight_layout()
    plt.savefig(output_folder + protocol + "-" + "-".join(cols) + ".png")
    plt.show()
            

def barplot(experiment, version, protocols):
    data_path = get_data_folder(experiment, "Zeek", version)
    output_folder = get_results_folder(experiment, "Zeek",
                                       version, "EDA")+"Train-Test Plots/"

    for protocol in protocols:
        print_progress(experiment, version, protocol.upper())
        for file_path in glob.glob(data_path+"/"+protocol+".csv", recursive=True):
            dataset = read_preprocessed(file_path)
            dataset = dataset[["Label"]]
            dataset["Label"] = np.where(dataset["Label"].str.contains("-"),
                                        dataset["Label"].str.split("-").str[0],
                                        dataset["Label"])

            for rs in range(RS):
                colname = "Train-Test " + str(rs)
                if rs == RS - 1:
                    colname = "Train-Test T"
                train, test, _, _ = train_test_split(dataset,
                                                     dataset["Label"],
                                                     stratify=dataset["Label"],
                                                     train_size=0.8,
                                                     random_state=rs)   
                _, val, _, _ = train_test_split(train,
                                                train["Label"],
                                                stratify=train["Label"],
                                                train_size=0.8,
                                                random_state=rs)       
                    
                valid_index = list(val.index)
                test_index = list(test.index)    
                
                dataset[colname] = -3
                dataset.loc[valid_index, colname] = -2         
                dataset.loc[test_index, colname] = -1
            
            dataset["Classes"] = dataset["Label"].astype('category').cat.codes
            dataset.sort_values(by=['Classes'],inplace=True, ignore_index = True)

            new_col = []
            for name, group in dataset.groupby("Label"):
                new_col.extend(list(group["Train-Test 0"].sort_values().values))
            dataset["Train Validation Test Fractions"] = new_col
            
            dataset["Classic situation 1 Fractions"] = new_col
            dataset["Classic situation 2 Fractions"] = new_col
            dataset["Experimental setup 1 Fractions"] = new_col
            dataset["Experimental setup 2 Fractions"] = new_col
            

            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -1)
            dataset.loc[condition1, "Classic situation 1 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -2)
            dataset.loc[condition1, "Classic situation 1 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -3)
            dataset.loc[condition1, "Classic situation 1 Fractions"] = -4

            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -1)
            dataset.loc[condition1, "Classic situation 2 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -2)
            dataset.loc[condition1, "Classic situation 2 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -3)
            dataset.loc[condition1, "Classic situation 2 Fractions"] = -4            
            
            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -1)
            dataset.loc[condition1, "Experimental setup 1 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -2)
            dataset.loc[condition1, "Experimental setup 1 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -3)
            dataset.loc[condition1, "Experimental setup 1 Fractions"] = -4

            condition1 = (dataset["Label"].str.startswith("DDoS")) & (dataset["Train Validation Test Fractions"] == -1)
            dataset.loc[condition1, "Experimental setup 2 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -2)
            dataset.loc[condition1, "Experimental setup 2 Fractions"] = -4
            condition1 = (dataset["Label"].str.startswith("DoS")) & (dataset["Train Validation Test Fractions"] == -3)
            dataset.loc[condition1, "Experimental setup 2 Fractions"] = -4
            
            vmap = dict(zip( dataset['Classes'], dataset['Label']))
            vc = dataset["Label"].value_counts().sort_index(ascending = True)
            
            cols = ["Classes"]
            plot_heatmap(dataset[cols], vmap, vc, cols, protocol, output_folder)
            
            cols_ = cols + ["Train Validation Test Fractions"]
            plot_heatmap(dataset[cols_], vmap, vc, cols_, protocol, output_folder)
            
            cols_train = cols_ + [c for c in dataset.columns if "Train-Test" in c]
            plot_heatmap(dataset[cols_train], vmap, vc, cols_train, protocol, output_folder)
            
            cols_train = cols + ["Classic situation 1 Fractions",
                                 "Classic situation 2 Fractions"]
            plot_heatmap(dataset[cols_train], vmap, vc, cols_train, protocol, output_folder)
            
            cols_train = cols_train + ["Experimental setup 1 Fractions",
                                       "Experimental setup 2 Fractions"]
            plot_heatmap(dataset[cols_train], vmap, vc, cols_train, protocol, output_folder)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            barplot(exp, vers, APP.selected_values["Files"])
