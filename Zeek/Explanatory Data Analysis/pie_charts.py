import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from application import Application, tk
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, print_progress
sns.set(font_scale=1.2)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def circle_diagram(experiment, version, protocols):
    data_path = get_data_folder(experiment, "Zeek", version)

    for protocol in protocols:
        print_progress(experiment, version, protocol.upper())
        for file_path in glob.glob(data_path+"/"+protocol+".csv", recursive=True):
            dataset = read_preprocessed(file_path)
            dataset["Label"] = np.where(dataset["Label"].str.contains('|'.join(["Benign","DDoS","DoS"])),
                                        dataset["Label"],"Other")
            
            
            if True:
                dataset["Label"] = np.where(dataset["Label"].str.contains("-"),
                                        dataset["Label"].str.split("-").str[0],
                                        dataset["Label"])
            else:
                dataset = dataset[dataset["Label"].str.startswith("DoS")]
            
            vc = dataset["Label"].value_counts()
            data = vc.values
            labels = list(vc.index)
            
            colors = []
            palette = sns.color_palette("Reds")
            i = 0
            for l in labels:
                if l == "Benign":
                    colors.append(sns.color_palette("Paired")[3])
                else:
                    colors.append(palette[i])
                    i = i + 1
            
            plt.figure(figsize =(10, 10))
            plt.pie(data, labels = labels, colors = colors, 
                    autopct = make_autopct(data))
            #patches, texts = plt.pie(data, colors=colors, startangle=0)
            #plt.legend(patches, labels, loc="best")
            plt.show()


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            circle_diagram(exp, vers, APP.selected_values["Files"])
