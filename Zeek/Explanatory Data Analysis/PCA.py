import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, print_progress, format_ML
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap

def PCA_plot(experiments, version, protocol):
    for exp in experiments:
        path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
        print_progress(exp, version, protocol.upper())
        try:
            dataset = read_preprocessed(path)
            dataset["Label"] =  dataset["Label"].astype("category").cat.codes
            print(dataset["Label"].value_counts())
            
            X, y, _, _ = format_ML(dataset)
            y_B = [i for i, y_i in enumerate(y) if y_i == 0]
            y_M = [i for i, y_i in enumerate(y) if y_i != 0]

            X = StandardScaler().fit(X).transform(X)
            print(pd.DataFrame(X).describe())
            
            X_B = X[y_B, :]
            X_M = X[y_M, :] 
                        
            model = PCA(n_components=3)
            model.fit(X_B)
            #print(model.explained_variance_ratio_)
            X = model.transform(X)
    
            X_B = X[y_B, :]
            X_M = X[y_M, :] 
            #cmap = ListedColormap(sns.color_palette("husl", 256).as_hex())
            plt.figure(figsize = (15, 15))
            sns.scatterplot(x = X_M[:,0], y = X_M[:,1], hue = y[y_M])
            #plt.xlim(-0.3,0.1)
            #plt.ylim(-1.2,0.4)
            plt.plot()
            #
            # for i in [0,1,2]:
            #     for j in [0,1,2]:
            #         for k in [0,1,2]:
            #             if i != j and j != k and k != i:
            #                 fig = plt.figure(figsize = (15,15))
            #                 ax = Axes3D(fig)
            #                 sc = ax.scatter(X[:,i], X[:,j], X[:,k], c = y, cmap=cmap)
            #                 plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)
            #                 plt.title(str(i) + " " + str(j) + " " + str(k))
            #                 plt.show()
        except FileNotFoundError:
            print("File-Not-Found")
    

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        for protocol in APP.selected_values["Files"]:
            PCA_plot(APP.selected_values["Experiments"], vers, protocol)