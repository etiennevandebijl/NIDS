import glob
import seaborn as sns
import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import get_data_folder, go_or_create_folder, get_results_folder
from Zeek.utils import read_preprocessed, format_ML
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D

def determine_color_dict(labels):
    colors = sns.color_palette("Paired",len(labels))
    color_dict = dict()
    for i, elem in enumerate(labels):
        color_dict[elem] = colors[i]
    color_dict["Benign"] = (0.9,0.9,0.9)
    return color_dict

def scatterplot_2d_PCA_components(X, y, index_B, index_M, labels, plot_M, plot_B,
                                  cp_1, cp_2, protocol, output_path):
    output_path = go_or_create_folder(output_path, "2d-plot")
    
    
    color_dict = determine_color_dict(labels)
    f = plt.figure(figsize=(15,7))
    ax = f.add_subplot(111)
    if plot_B:
        sns.scatterplot(x = X[index_B,cp_1], y = X[index_B,cp_2], hue = y[index_B], 
                            ax=ax, palette = color_dict, s = 15)
    if plot_M:
        sns.scatterplot(x = X[index_M,cp_1], y = X[index_M,cp_2], hue = y[index_M], 
                            ax=ax, palette = color_dict, s = 40)

    plt.xlabel("Principal component " + str(cp_1 + 1))
    plt.ylabel("Principal component " + str(cp_2 + 1))
    plt.xlim(-5,5)
    plt.ylim(-5,6)
    plt.tight_layout()
    plt.savefig(output_path + protocol + "-PCA-PC " + str(cp_1) + "-PC " + str(cp_2) + \
                ".png")
    
    plt.plot()

def scatterplot_3d_PCA_components(X, y, index_B, index_M, labels, plot_B,
                           cp_1, cp_2, cp_3, protocol, output_path):
    output_path = go_or_create_folder(output_path, "3d-plot")
    
    color_dict = determine_color_dict(labels)
    
    fig = plt.figure(figsize = (15,15))
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    
    for label, color in color_dict.items():
        if not plot_B and label == "Benign":
            continue
        indices = [i for i,v in enumerate(y) if v == label]
        ax.scatter(X[indices, cp_1], X[indices, cp_2], X[indices, cp_3], 
                   label = label, color=color)    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    
    ax.set_xlabel("Principal component " + str(cp_1 + 1))
    ax.set_ylabel("Principal component " + str(cp_2 + 1))
    ax.set_zlabel("Principal component " + str(cp_3 + 1))
    
    plt.savefig(output_path + protocol + "-PCA-PC " + str(cp_1) + "-PC " + str(cp_2) + \
                "-PC " + str(cp_3) + ".png")
    
    plt.show()

def perform_dimension_reduction(X, index_B):
    model = PCA(n_components=3)
    model.fit(X[index_B, :])
    print(model.explained_variance_ratio_)
    X = model.transform(X)
    return X

def PCA_plot(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version)
    output_folder = get_results_folder(experiment, "BRO", version, "EDA")
    output_folder = go_or_create_folder(output_folder, "PCA-Dimension-Reduction")

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + protocol + ".csv", recursive=True):            
            dataset = read_preprocessed(file_path)
            X, y, _, labels = format_ML(dataset)

            index_B = dataset.index[dataset['Label'] == "Benign"].tolist()
            index_M = dataset.index[dataset['Label'] != "Benign"].tolist()
            
            # Step 1: Scale data to normal distribution
            X = StandardScaler().fit(X).transform(X)
            
            #Step 2 fit PCA on normal traffic and transform all data
            X = perform_dimension_reduction(X, index_B)
            
            for i,j in [[0,1],[0,2],[1,2]]:
                scatterplot_2d_PCA_components(X, y, index_B, index_M, labels, True, 
                                          True, i, j, protocol, output_folder)
            
            for i in [0,1,2]:
                for j in [0,1,2]:
                    for k in [0,1,2]:
                        if i != j and i != k and j != k:
                            scatterplot_3d_PCA_components(X, y, index_B, index_M, 
                                                          labels, False, i, j, k, 
                                                          protocol, output_folder)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            PCA_plot(exp, vers, APP.selected_values["Files"])