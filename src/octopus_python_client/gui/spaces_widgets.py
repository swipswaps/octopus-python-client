import tkinter as tk
from tkinter import ttk

from octopus_python_client.actions import ACTIONS_DICT, MIGRATION_LIST
from octopus_python_client.common import Common


class SpacesWidgets(tk.Frame):
    def __init__(self, parent, server: Common, source: Common):
        super().__init__(parent)
        self.server = server
        self.source = source
        self.space_id_variable = None
        self.source_space_id_variable = None
        self.update_step()

    def update_step(self):
        self.space_id_variable = None
        self.source_space_id_variable = None
        tk.Label(self, text=f"{self.server.config.action} ({ACTIONS_DICT.get(self.server.config.action)})",
                 bd=2, relief="groove").grid(sticky=tk.W)
        if self.server.config.action in MIGRATION_LIST:
            self.source_space_id_variable = self.set_spaces_frame(server=self.source)
            ttk.Separator(self, orient=tk.HORIZONTAL).grid(sticky=tk.EW)
            tk.Label(self, text=f"\u21D3     \u21D3     \u21D3     \u21D3     \u21D3      {self.server.config.action}"
                                f"      \u21D3     \u21D3     \u21D3     \u21D3     \u21D3",
                     bd=2, relief="groove").grid(sticky=tk.EW)
            ttk.Separator(self, orient=tk.HORIZONTAL).grid(sticky=tk.EW)
        self.space_id_variable = self.set_spaces_frame(server=self.server)

    def set_spaces_frame(self, server: Common):
        spaces_frame = tk.Frame(self)
        tk.Label(spaces_frame, text=f"Select a space:", bd=2).grid(row=0, sticky=tk.W, columnspan=2)
        space_id_variable = tk.StringVar()
        space_id_variable.set(server.config.space_id)
        space_id_list = list(server.config.spaces.keys())
        space_id_list.sort(key=lambda sid: int(sid.split("-")[1]))
        no_items_per_row = 4
        for index, space_id in enumerate(space_id_list):
            tk.Radiobutton(spaces_frame, text=f"{server.config.spaces.get(space_id)}",
                           variable=space_id_variable, value=space_id, justify=tk.LEFT, command=lambda *args: None) \
                .grid(row=1 + int(index / no_items_per_row), column=index % no_items_per_row, sticky=tk.W, columnspan=1)
        spaces_frame.grid(sticky=tk.W)
        return space_id_variable

    def process_config(self):
        if self.source_space_id_variable:
            self.source.config.space_id = self.source_space_id_variable.get()
            self.source.config.save_config()
        self.server.config.space_id = self.space_id_variable.get()
        self.server.config.save_config()
        return True
