import glob
import pandas as pd

from project_paths import get_results_folder
from ML.Unsupervised.output import create_figures
from application import Application, tk

def make_figures_usl(experiment, version, protocols):
    target_folders = get_results_folder(experiment, "BRO", version, "Unsupervised")

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(target_folders + protocol + "**/anomaly-scores.csv", recursive = True):
            
            df = pd.read_csv(file_path, sep = ";", decimal = ",")
            df["ts"] = pd.to_datetime(df["ts"]) 
            output_path = file_path.replace("anomaly-scores.csv","")
            create_figures(df, output_path)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            make_figures_usl(exp, vers, APP.selected_values["Files"])







