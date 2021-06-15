import glob
import time
import warnings

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import read_preprocessed
from Methods.Pynod.change import distances_Event_Change
from Methods.Pynod.output import output
from application import Application, tk

warnings.filterwarnings("ignore")

def graph_distance(experiment, protocols, freq, delta, weighted = False):
    input_path = get_data_folder(experiment, "BRO", "5_Graph")
    output_path = get_results_folder(experiment, "BRO", "5_Graph", "")[:-1]

    for protocol in protocols:
        print("---" + experiment + "--5_Graph--" + protocol.upper() + "----")
        time.sleep(1)
        for file_path in glob.glob(input_path + protocol + "-edges-" + freq + ".csv", recursive=True):
            df = read_preprocessed(file_path)
            ts_list, df_dist, labels = distances_Event_Change(df, delta, freq, weighted)

            output_path_ = go_or_create_folder(output_path, protocol)
            output_path_ = go_or_create_folder(output_path_, freq)
            output_path_ = go_or_create_folder(output_path_, "Delta" + str(delta))
            output(df_dist, labels, ts_list, output_path_)

FREQ = '5s'

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=6)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        graph_distance(exp, APP.selected_values["Files"], FREQ, 1, False)
       # graph_distance(exp, APP.selected_values["Files"], FREQ, 1, True)
