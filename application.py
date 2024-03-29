#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Application to select Experiments/ Versions / Protocols."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import os
import glob
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from project_paths import DATA_PATH, get_data_folder


if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class Application(tk.Frame):
    """Application for selection datasets, versions and protocols.

    This class starts the Tkinter interface to select datasets which can be
    found in the PROJECT_PATH.
    """

    def __init__(self, master=None, v_setting=0):
        super().__init__(master)
        self.master = master
        self.master.title("Parameters")
        self.pack()
        self.selected_values = {}
        self.master.geometry("500x360+300+300")
        self.settings = self.options_list(v_setting)
        self.create_widgets()

    def options_list(self, v_setting=0):
        """Option list to select versions instead of showing all."""
        settings = {"Experiments": os.listdir(DATA_PATH)}
        f_format = "*.csv"

        if v_setting == 0:
            f_format = "*/*.log"
            settings["Version"] = ["1_Raw"]
        elif v_setting == 1:
            settings["Version"] = ["2_Preprocessed", "2_Preprocessed_DDoS",
                                   "2_Preprocessed_Web", "3_Downsampled"]
        elif v_setting == 2:
            settings["Version"] = ["4_Feature_Reduction"]
        elif v_setting == 3:
            settings["Version"] = ["5_Graph"]
        elif v_setting == 4:
            settings["Version"] = ["2_Preprocessed"]
        elif v_setting == 5:
            settings["Version"] = ["2_Preprocessed", "3_Downsampled"]
        elif v_setting == 6:
            settings["Version"] = ["4_Feature_Reduction"]
        else:
            settings["Version"] = [v_setting]

        files = []
        for exp in os.listdir(DATA_PATH):
            for vers in settings["Version"]:
                path = get_data_folder(exp, "Zeek", vers)
                for file_path in glob.glob(path + f_format, recursive=False):
                    base = Path(file_path).stem
                    files.append(base)
        settings["Files"] = sorted(list(set(files)), key=len)
        if v_setting == 6:
            settings["Version"] = ["5_Graph"]
        return settings

    def create_widgets(self):
        """Widget creator."""
        col = 0
        max_row = 0
        self.variables = {}
        for title, list_opt in self.settings.items():
            tk.Label(self, text=title,
                     font='Helvetica 10 bold').grid(row=0, column=col)

            box = {}
            for index, opt in enumerate(list_opt):
                box[opt] = tk.IntVar()
                # if (len(list_opt) == 1) | (title == "Files"):
                #     box[opt] = tk.IntVar(value=1)
                tk.Checkbutton(self, text=opt,
                               variable=box[opt]).grid(row=index+1, column=col)
                max_row = max(max_row, index+1)
            self.variables[title] = box
            col += 1

        # Buttons
        tk.Button(self, text="ACCEPT", fg="blue",
                  command=self.process_input).grid(row=max_row + 1,
                                                   column=len(self.settings)-1)
        tk.Button(self, text="QUIT", fg="red",
                  command=self.master.destroy).grid(row=max_row + 1,
                                                    column=0)

    def process_input(self):
        """Process input of the selected options."""
        missing_input = []
        self.selected_values = {}
        for title, checkboxes in self.variables.items():
            list_items = [k for k, v in checkboxes.items() if v.get() == 1]
            if len(list_items) == 0:
                missing_input.append(title)
            else:
                self.selected_values[title] = list_items

        if len(missing_input) > 0:
            message = "No " + " + ".join(missing_input) + " selected."
            messagebox.showerror(title="Invalid error", message=message)
        else:
            answer = messagebox.askquestion(title="Confirmation",
                                            message="Do you confirm?")
            if answer == "yes":
                self.master.destroy()


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    print(APP.selected_values)
