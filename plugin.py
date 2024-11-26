from tkinter import messagebox
import os
import json
import shutil

class Interaction(object):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
    def Error(self, message):
        messagebox.showerror("Error from %s" % self.plugin_name, message)
    def Fatal(self, message):
        messagebox.showerror("Fatal from %s" % self.plugin_name, message)
        exit(0)
    def Warn(self, message):
        messagebox.showwarning("Warning from %s" % self.plugin_name, message)
    def Note(self, message):
        messagebox.showinfo("Note from %s" % self.plugin_name, message)


def init(programdict, namespaces, pjset, projectpath):
    with open(os.path.join(programdict,"plugins","plugin_list.json")) as f:
        lists = json.load(f)
    plugin_list = []
    for plugin in lists:
        with open(os.path.join(programdict,"plugins",plugin,"setting.json")) as f:
            zc_data = json.load(f)
        plugin_list.append(zc_data)
        for i in zc_data["algorithm"]:
            ...