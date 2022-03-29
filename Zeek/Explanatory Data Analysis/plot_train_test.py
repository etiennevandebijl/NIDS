import glob
import seaborn as sns
import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, print_progress
from sklearn.model_selection import train_test_split
sns.set(font_scale=1.2)
from sklearn.model_selection import StratifiedShuffleSplit

from Zeek.utils import format_ML

def barplot(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version)

    for protocol in protocols:
        print_progress(experiment, version, protocol.upper())
        

        for file_path in glob.glob(data_path+"/"+protocol+".csv", recursive=True):
            dataset = read_preprocessed(file_path)
            
            df_y = dataset[["Label"]]
            for rs in range(3):
                colname = "Train-Test "+str(rs)
                if rs == 2:
                    colname = "Train-Test T"
                df_y[colname] = 0
                train, test, _, _ = train_test_split(dataset, dataset["Label"],
                                                          stratify=dataset["Label"],
                                                          train_size=0.8,
                                                          random_state=rs)
                df_y.loc[list(test.index), colname] = 2
                
                splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
                X, y, _, _ = format_ML(train)
                for train_index, test_index in splitter.split(X, y):
                    validation_index = train.iloc[test_index].index
                    df_y.loc[list(validation_index), colname] = 1
            
            df_y["Data"] = df_y["Label"].astype('category').cat.codes + 3
            
            vc = df_y["Label"].value_counts().sort_index(ascending = True)
            
            df_y = df_y.sort_values(by=['Label'])
            
            new_col = []
            for name, group in df_y.groupby("Label"):
                new_col.extend(list(group["Train-Test 0"].sort_values().values))
            df_y["Train Validation Test Fractions"] = new_col
            
            df_y.set_index("Label",inplace = True)

            vmap = {0:"Train (64%)", 1:"Validation (16%)", 2: "Test (20%)"}

            plt.figure(figsize = (25, 16))

            cmap = [sns.color_palette("Paired")[3],
                    sns.color_palette("Set2")[5],
                    sns.color_palette("Paired")[5]
                    ]
            cmap = cmap + sns.color_palette("deep", len(df_y["Data"].unique()))
            n = len(vmap)
                        
            ax = sns.heatmap(df_y.T.sort_index(), cmap=cmap)
            ax.axhline(1, color='white', lw=10)
            ax.axhline(2, color='white', lw=10)

            index = 0
            for val, cnt in vc.iteritems():
                index = index + cnt
                ax.axvline(index, color='white', lw=10)

            colorbar = ax.collections[0].colorbar
            r = colorbar.vmax - (colorbar.vmin + 2)
            colorbar.set_ticks([colorbar.vmin + 0.5 * r / (n) + r * i / (n) for i in range(n)])
            colorbar.set_ticklabels(list(vmap.values()))

            plt.xticks([], [])
            plt.xlabel("Instance")
            plt.yticks(rotation=0) 
            plt.show()

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            barplot(exp, vers, APP.selected_values["Files"])