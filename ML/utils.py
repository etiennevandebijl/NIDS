import os
import json
import time


def rename_and_select_labels(df_, group_labels, selected_labels,
                             output_path=None, folder_name="labels_info"):
    df = df_.copy()
    for new_label_name, label_group in group_labels.items():
        df.loc[df["Label"].isin(label_group), 'Label'] = new_label_name
    df = df[df["Label"].isin(selected_labels)]

    if output_path is not None:
        dict_labels = {"group_labels": group_labels,
                       "selected_labels": selected_labels}
        with open(output_path + folder_name + '.json', 'w') as f:
            json.dump(dict_labels, f)
    return df


def create_output_path(output_path, protocol, folder):
    time.sleep(1)
    print(folder)
    output_path = output_path + protocol + "/" + folder + '/'
    os.makedirs(output_path, exist_ok=True)
    return output_path
