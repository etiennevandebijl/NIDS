import glob
import seaborn as sns
import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, format_ML
from sklearn.preprocessing import StandardScaler

from sklearn.manifold import TSNE

def PCA_plot(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version)
    
    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + protocol + ".csv", recursive=True):            
            dataset = read_preprocessed(file_path)
            dataset = dataset.sample(frac = 0.01).reset_index()
            
            X, y, _, labels = format_ML(dataset)

            index_B = dataset.index[dataset['Label'] == "Benign"].tolist()
            index_M = dataset.index[dataset['Label'] != "Benign"].tolist()
            
            # Step 1: Scale data to normal distribution
            X = StandardScaler().fit(X).transform(X)
            
            #Step 2 fit PCA on normal traffic and transform all data
            model = TSNE(n_components=3)
            X = model.fit_transform(X)
 
            colors = sns.color_palette("Paired",len(labels))
            color_dict = dict()
            for i, elem in enumerate(labels):
                color_dict[elem] = colors[i]
            color_dict["Benign"] = (0.9,0.9,0.9)
            
            f = plt.figure(figsize=(15,7))
            ax = f.add_subplot(111)
            sns.scatterplot(x = X[index_B,0], y = X[index_B,1], hue =y[index_B], ax=ax, palette = color_dict, s = 15)
            sns.scatterplot(x = X[index_M,0], y = X[index_M,1], hue =y[index_M], ax=ax, palette = color_dict, s = 40)

            plt.plot()


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            PCA_plot(exp, vers, APP.selected_values["Files"])