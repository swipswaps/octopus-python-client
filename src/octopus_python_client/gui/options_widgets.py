import tkinter as tk

from octopus_python_client.actions import Actions
from octopus_python_client.common import Common, inside_space_clone_types


class OptionsWidgets(tk.Frame):
    def __init__(self, parent, server: Common, source: Common):
        super().__init__(parent)
        self.server = server
        self.source = source
        self.types_var_dict = {}
        self.update_step()

    def update_step(self):
        tk.Label(self, text=f"{self.server.config.action} ({Actions.ACTIONS_DICT.get(self.server.config.action)})",
                 bd=2, relief="groove").grid(sticky=tk.W)
        self.set_types_frame()

    def select_all_types(self):
        for item_type in inside_space_clone_types:
            self.types_var_dict.get(item_type).set("1")

    def deselect_all_types(self):
        for item_type in inside_space_clone_types:
            self.types_var_dict.get(item_type).set("0")

    def set_types_frame(self):
        self.types_var_dict = {}
        types_frame = tk.Frame(self)
        tk.Label(types_frame, text=f"Select the item types you want", bd=2).grid(row=0, sticky=tk.W, columnspan=2)
        tk.Button(types_frame, text='Select all types', command=self.select_all_types) \
            .grid(row=0, column=2, sticky=tk.W, columnspan=1)
        tk.Button(types_frame, text='Deselect all types', command=self.deselect_all_types) \
            .grid(row=0, column=3, sticky=tk.W, columnspan=1)
        for index, item_type in enumerate(inside_space_clone_types):
            self.types_var_dict[item_type] = tk.StringVar()
            tk.Checkbutton(types_frame, text=item_type, variable=self.types_var_dict.get(item_type)) \
                .grid(row=int(1 + index / 5), column=index % 5, sticky=tk.W)
            if item_type in self.server.config.types:
                self.types_var_dict.get(item_type).set("1")
            else:
                self.types_var_dict.get(item_type).set("0")
        types_frame.grid(sticky=tk.W)

    def process_config(self):
        self.server.config.types = []
        for item_type in inside_space_clone_types:
            if self.types_var_dict.get(item_type).get() == "1":
                self.server.config.types.append(item_type)
        self.server.config.save_config()
        return True