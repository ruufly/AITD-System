# Copyright 2024 Zhu jingrui, Hu Gaoyuan, Deng Yutong, et al

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

try:
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
except Exception:
    pass
import sys
import tkinter
from tkinter import *
from tkinter import messagebox, filedialog, ttk
import pickle
import json
from PIL import Image, ImageTk
import yaml
import aitd
import shutil
import pyglet
import numpy as np
import time

# from copy import deepcopy
import matplotlib.pyplot as plt

# import matplotlib.font_manager
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import ConnectionPatch

root = Tk(className="AITD_System")
root.title("AITD System")
root.configure(background="white")
root.update()
scx, scy = root.winfo_screenwidth(), root.winfo_screenheight()
wdx, wdy = root.winfo_width(), root.winfo_height()
root.minsize(int(scx / 2), int(scy / 1.6))
# root.maxsize(int(scx / 2), int(scy / 1.8))

programdict = os.path.dirname(os.path.abspath(__file__))

root.iconbitmap(os.path.join(programdict, "data", "icons", "icon.ico"))

pyglet.font.add_file(
    os.path.join(programdict, "data", "fonts", "SourceHanSansSC-Normal.otf")
)
# pyglet.font.add_file(os.path.join(programdict,"data","fonts","OPPOSans-Regular.ttf"))


plt.rcParams["font.sans-serif"] = "SimHei"
# SourceHanSansSC = matplotlib.font_manager.FontProperties(fname=os.path.join(programdict, "data", "fonts", "SourceHanSansSC-Normal.otf"), size=14)

projectpath = ""
nowopen = False
pjset = {}
namespaces = {}

symboltree = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightAccountTreeOutlineRounded.png",
        )
    ).resize((20, 20))
)
symbolcomputer = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightDesktopWindowsOutlineSharp.png",
        )
    ).resize((20, 20))
)
symbolsetting = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightDisplaySettingsOutlineRounded.png",
        )
    ).resize((20, 20))
)
symbolDNA = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightGeneticsRounded.png",
        )
    ).resize((20, 20))
)
symbolsearch = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict, "data", "icons", "MaterialSymbolsLightManageSearchRounded.png"
        )
    ).resize((20, 20))
)
symbolsketch = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict, "data", "icons", "MaterialSymbolsLightDrawOutlineRounded.png"
        )
    ).resize((20, 20))
)
symbolplugin = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightReceiptLongOutlineRounded.png",
        )
    ).resize((20, 20))
)
symbolunchecked = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict, "data", "icons", "MaterialSymbolsLightCheckBoxOutlineBlank.png"
        )
    ).resize((20, 20))
)
symbolchecked = ImageTk.PhotoImage(
    Image.open(
        os.path.join(
            programdict,
            "data",
            "icons",
            "MaterialSymbolsLightCheckBoxOutlineRounded.png",
        )
    ).resize((20, 20))
)

with open(os.path.join(programdict, "data", "setting.dat"), "rb") as f:
    try:
        config = pickle.load(f)
    except EOFError:
        config = {
            "language": "en",
            "defaultComparator": "ComparatorList::needleman-wunsch",
            "defaultMatrix": "MatrixList::transition-transversion",
            "defaultGap": -2,
        }
        with open(os.path.join(programdict, "data", "setting.dat"), "wb") as f:
            pickle.dump(config, f)

with open(os.path.join(programdict, "data", "en.yml"), "r", encoding="utf-8") as f:
    endata = yaml.safe_load(f.read())

langdata = endata
defaultComparator = config["defaultComparator"]
defaultMatrix = config["defaultMatrix"]
defaultGap = config["defaultGap"]


def getlang(word):
    """
    获取语言文本

    Args:
        word (str): 文本名（可在data\\xxx.yml中看到）

    Returns:
        word (str): 文本内容
    """
    if word in langdata:
        return langdata[word]
    elif word in endata:
        return endata[word]
    else:
        messagebox.showerror(
            "AITD System",
            "Unable to find corresponding language information: %s" % word,
        )
        exit()


def refresh_setting():
    """
    刷新语言设置

    Returns:
        isset (bool): 是否成功刷新
    """
    global langdata
    try:
        with open(
            os.path.join(programdict, "data", "%s.yml" % config["language"]),
            "r",
            encoding="utf-8",
        ) as f:
            langdata = yaml.safe_load(f.read())
    except Exception as e:
        messagebox.showerror(
            "AITD System", "Unable to load language file: %s.yml" % (config["language"])
        )
        langdata = endata
        return False
    return True


refresh_setting()

ismainfat = False
nowsthopen = ""

topf = Frame(root, bg="black")
topf.place(relheight=0.15, relwidth=1, relx=0, rely=0)

sidef = Frame(root, bg="white")
sidef.place(relheight=0.85, relwidth=0.25, relx=0, rely=0.15)

mainf = Frame(root, bg="white")
mainf.place(relheight=0.85, relwidth=0.75, relx=0.25, rely=0.15)

tfff = Frame(sidef, bg="white")
tfff.place(relheight=0.8, relwidth=1, relx=0, rely=0)

treefile = ttk.Treeview(tfff, show="tree")
treefile.tag_configure("fggrey", foreground="grey")

vbtf = ttk.Scrollbar(tfff, orient=VERTICAL, command=treefile.yview)
vbtf.pack(side=RIGHT, fill=Y)
vbtfx = ttk.Scrollbar(tfff, orient=HORIZONTAL, command=treefile.xview)
vbtfx.pack(side=BOTTOM, fill=X)

treefile.config(yscrollcommand=vbtf.set)
treefile.config(xscrollcommand=vbtfx.set)
treefile.pack(fill=BOTH, expand=1)


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


def getit(name):
    if type(name) != str:
        return name
    else:
        if name[0] == "@":
            if type(namespaces[name[1:]]) == str:
                return '"' + namespaces[name[1:]] + '"'
            else:
                return namespaces[name[1:]]
        elif name[0] == "#":
            return name[1:]
        else:
            return '"' + name + '"'


with open(os.path.join(programdict, "plugins", "plugin_list.json")) as f:
    lists = json.load(f)
plugin_list = {}


def isPlugin(name):
    return name in plugin_list


for plugin in lists:
    with open(os.path.join(programdict, "plugins", plugin, "setting.json")) as f:
        zc_data = json.load(f)
    plugin_list[plugin] = zc_data
    for i in zc_data["settings"]:
        namespaces[i] = zc_data["settings"][i]
    for i in zc_data["algorithm"]:
        exec("import plugins.%s.%s" % (plugin, zc_data["algorithm"][i]["file"]))
        exec(
            'setattr(aitd.xerlist.%s,"%s",%s)'
            % (
                zc_data["algorithm"][i]["in"],
                "%s::%s" % (plugin, i),
                "plugins.%s.%s.%s"
                % (
                    plugin,
                    zc_data["algorithm"][i]["file"],
                    zc_data["algorithm"][i]["prototype"],
                ),
            )
        )
    if zc_data["init"]["open"]:
        exec("import plugins.%s.%s" % (plugin, zc_data["init"]["file"]))
        exec(
            "plugins.%s.%s.%s("
            % (plugin, zc_data["init"]["file"], zc_data["init"]["prototype"])
            + "".join(
                ("%s=%s," % (i, getit(zc_data["init"]["args"][i])))
                for i in zc_data["init"]["args"]
            )
            + 'interaction=Interaction("%s"),iswindow=True)' % plugin
        )


# for i in range(20): treefile.insert("",0,str(i),text=str(i))


def displaytree(data, opened):
    with open(os.path.join(projectpath, data["file"]), "rb") as f:
        treedata = pickle.load(f)
    elbl = Label(mainf, text=getlang("elbl"), bg="white")
    elbl.place(x=5, y=5)
    rtll = Text(mainf, bg="white")
    rtll.place(y=35, relwidth=1, relheight=0.4)
    rtll.insert(END, str(treedata))
    rtll.config(state=DISABLED)
    secuffr = Frame(mainf, bg="white")
    lbee1 = Text(secuffr)
    lbee1.pack(fill=BOTH, expand=1)
    lbee1.insert(END, "CODE: %s ; OPPOSING: " % opened)
    for i in data["opposing"]:
        lbee1.insert(END, i + ", ")
    lbee1.insert(
        END,
        "; ALGORITHM: %s ." % (data["algorithm"]),
    )
    lbee1.config(state=DISABLED)
    secuffr.place(relheight=0.08, relwidth=1, relx=0, rely=0.9)
    root.update()


def displaysktch(data, opened):
    global projectpath
    global sktchphoto
    global ismainfat
    ismainfat = False
    try:
        sktchphoto = ImageTk.PhotoImage(
            Image.open(os.path.join(projectpath, data["file"]))
        )
    except OSError as e:
        messagebox.showerror("AITD System", e)
        return
    showskch = Label(mainf, image=sktchphoto, bg="linen")
    showskch.place(relheight=0.8, relwidth=1, relx=0, rely=0)

    def exportimg(*args):
        path = filedialog.asksaveasfilename(
            title=getlang("exportimg"),
            filetypes=[("PNG", os.path.splitext(data["file"])[1])],
            defaultextension=os.path.splitext(data["file"])[1],
        )
        if not path:
            return
        try:
            shutil.copy(os.path.join(projectpath, data["file"]), path)
        except Exception:
            messagebox.showerror("AITD System", getlang("errorsave"))
            return
        messagebox.showinfo("AITD System", getlang("success"))

    secufr = Frame(mainf, bg="white")
    seqbut1 = ttk.Button(secufr, text=getlang("exportimg"), command=exportimg)
    seqbut1.place(x=10, y=10)
    # seqbut2 = ttk.Button(secufr, text=getlang("occlr"), command=cuc)
    # seqbut2.grid(row=1, column=2, padx=(10, 0), pady=10)
    # seqbut3 = ttk.Button(secufr, text=getlang("deldeq"), command=delleq)
    # seqbut3.grid(row=1, column=3, padx=(10, 0), pady=10)
    secufr.place(relheight=0.1, relwidth=1, relx=0, rely=0.8)
    secuffr = Frame(mainf, bg="white")
    lbee1 = Text(secuffr)
    lbee1.pack(fill=BOTH, expand=1)
    lbee1.insert(END, "CODE: %s ; COMPOSITION: " % opened)
    for i in data["composition"]:
        lbee1.insert(END, i + ", ")
    lbee1.insert(
        END,
        "; FROM: %s ; RENDERER: %s ; FILE_EXTENSION: %s"
        % (data["from"], data["renderer"], os.path.splitext(data["file"])[1]),
    )
    lbee1.config(state=DISABLED)
    secuffr.place(relheight=0.08, relwidth=1, relx=0, rely=0.9)


def displayali(data, opened):
    global ismainfat
    global projectpath
    global alit
    global isdisplayseqcolored
    isdisplayseqcolored = True
    ismainfat = True
    with open(os.path.join(projectpath, data["file"]), "r") as f:
        alit = f.readlines()
    alit[0] = alit[0].replace("\n", "")

    topmainf = Frame(mainf, bg="white")

    seqfr = Frame(topmainf)
    seqtext = Text(
        seqfr, wrap=NONE, bg="black", selectbackground="white", height=3
    )  # , font=("OPPO Sans",10))  #, yscrollincrement=20)
    seqtext.bind("<Return>", lambda *args: "break")
    seqtext.tag_config("tag_A", foreground="chocolate")
    seqtext.tag_config("tag_T", foreground="blueviolet")
    seqtext.tag_config("tag_C", foreground="darkgreen")
    seqtext.tag_config("tag_G", foreground="dodgerblue")
    seqtext.tag_config("tag_NONE", foreground="aqua")
    seqtext.tag_config("tag_GOT", foreground="green")
    seqtext.tag_config("tag_UNGOT", foreground="yellow")
    seqtext.tag_config("tag_STOPAT", foreground="red")

    seqtextvbtf = ttk.Scrollbar(seqfr, orient=HORIZONTAL, command=seqtext.xview)
    seqtext.configure(xscrollcommand=seqtextvbtf.set)
    seqtextvbtf.pack(side=BOTTOM, fill=X)
    seqtext.pack(fill=BOTH, expand=1)

    def showseq(seq, seqtext, color=True):
        global isdisplayseqcolored
        if color:
            for i in range(len(seq)):
                try:
                    if seq[i] == "-":
                        seqtext.insert(END, seq[i], "tag_NONE")
                    else:
                        try:
                            seqtext.insert(END, seq[i], "tag_%s" % seq[i])
                        except Exception:
                            seqtext.insert(END, seq[i])
                    if i % 200 == 0:
                        root.update()
                except Exception:
                    return
        else:
            for i in range(len(seq)):
                try:
                    seqtext.insert(END, seq[i])
                    if i % 200 == 0:
                        root.update()
                except Exception:
                    return
        isdisplayseqcolored = color
        # seqtext.config(state=DISABLED)

    seqtext.config(state=NORMAL)
    showseq(alit[0], seqtext, isdisplayseqcolored)
    seqtext.insert(END, "\n")
    # print(alit)
    for i in range(len(alit[0])):
        if alit[0][i] == "-" or alit[1][i] == "-":
            seqtext.insert(END, ":", "tag_STOPAT")
        elif alit[0][i] != alit[1][i]:
            seqtext.insert(END, "|", "tag_UNGOT")
        else:
            seqtext.insert(END, "|", "tag_GOT")
        if i % 200 == 0:
            root.update()
    seqtext.insert(END, "\n")
    # print(alit)
    showseq(alit[1], seqtext, isdisplayseqcolored)
    seqtext.config(state=DISABLED)

    seqfr.place(relwidth=1, relx=0, rely=0)

    topmainf.place(relheight=0.2, relwidth=1, relx=0, rely=0)

    scoredistance = Frame(mainf, bg="white")

    with open(os.path.join(projectpath, data["data"]), "r") as f:
        datadata = f.readlines()
        Label(
            topmainf,
            text=getlang("score") + ": %d" % (int(datadata[0].replace("\n", ""))),
            bg="white",
        ).place(relx=0, rely=0.7)
        Label(
            topmainf,
            text=getlang("distance") + ": %d" % (int(datadata[1].replace("\n", ""))),
            bg="white",
        ).place(relx=0.25, rely=0.7)

    eadd, edefect, ereplace, etransition, etransversion, esuccess = 0, 0, 0, 0, 0, 0

    datatype = namespaces[data["opposing"][0]]["type"]

    for i in range(len(alit[0])):
        if alit[0][i] == "-" and alit[1][i] != "-":
            eadd += 1
        elif alit[0][i] != "-" and alit[1][i] == "-":
            edefect += 1
            # print(f"edefect-{alit[0][i]}-{alit[1][i]}")
        elif alit[0][i] != alit[1][i]:
            ereplace += 1
            # print(f"ereplace-{alit[0][i]}-{alit[1][i]}")
            if datatype == "gene" or datatype == "genome":
                if (
                    (alit[0][i] == "A" and alit[1][i] == "G")
                    or (alit[0][i] == "G" and alit[1][i] == "A")
                    or (alit[0][i] == "C" and alit[1][i] == "T")
                    or (alit[0][i] == "T" and alit[1][i] == "C")
                ):
                    etransition += 1
                if (
                    (alit[0][i] == "A" and alit[1][i] == "C")
                    or (alit[0][i] == "C" and alit[1][i] == "A")
                    or (alit[0][i] == "G" and alit[1][i] == "T")
                    or (alit[0][i] == "T" and alit[1][i] == "G")
                ):
                    etransversion += 1
        else:
            esuccess += 1

    y = np.array([eadd, edefect, ereplace, esuccess])

    if datatype == "gene" or datatype == "genome":
        yn = np.array([etransition, etransversion])

    plt.clf()

    figure = plt.figure(num=2, figsize=(7, 4), dpi=80, frameon=True)

    ax1 = figure.add_subplot(121)
    ax1.set_title(getlang("match"))

    ax1.pie(
        y,
        labels=[
            getlang("insertion"),
            getlang("deletion"),
            getlang("point_mutation"),
            getlang("msuccess"),
        ],
        colors=["#d5695d", "#5d8ca8", "#65a479", "#39c5bb"],
        autopct="%.2f%%",
        startangle=0,
        radius=1.1,
        pctdistance=0.6,
        explode=(0, 0, 0, 0.2),
        shadow=True,
    )

    # print(eadd, edefect, ereplace, etransition, etransversion)

    if (datatype == "gene" or datatype == "genome") and (
        etransition != 0 or etransversion != 0
    ):
        ax2 = figure.add_subplot(122)
        ax2.set_title(getlang("inallofpm"))
        ax2.pie(
            yn,
            colors=["khaki", "olive"],
            autopct="%.2f%%",
            labels=[getlang("transition"), getlang("transversion")],
            radius=0.5,
            shadow=True,
        )

    # plt.title("RUNOOB Pie Test")
    drawpic_canvas = FigureCanvasTkAgg(figure, master=scoredistance)
    drawpic_canvas.draw()
    drawpic_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    scoredistance.place(relheight=0.6, relwidth=1, relx=0, rely=0.2)

    secuffr = Frame(mainf, bg="white")
    lbee1 = Text(secuffr)
    lbee1.pack(fill=BOTH, expand=1)
    lbee1.insert(END, "CODE: %s ; OPPOSING: " % opened)
    for i in data["opposing"]:
        lbee1.insert(END, i + ", ")
    lbee1.insert(
        END,
        "; ALGORITHM: %s ; MATRIX: %s ." % (data["algorithm"], data["matrix"]),
    )
    lbee1.config(state=DISABLED)
    secuffr.place(relheight=0.08, relwidth=1, relx=0, rely=0.9)

    root.update()


def displayseq(data, opened):
    # global nowsthopen
    global ismainfat
    global projectpath
    global isdisplayseqcolored
    global pjset
    isdisplayseqcolored = True
    # if nowsthopen == opened:
    #     return
    # nowsthopen = opened
    # if ismainfat:
    #     if not messagebox.askyesno("AITD System", getlang("reallyopen")):
    #         return
    global seqt
    with open(os.path.join(projectpath, data["file"]), "r") as f:
        seqt = f.read()
    print(len(seqt))
    if len(seqt) > 100000:
        if not messagebox.askyesno("AITD System", getlang("seqtoolong")):
            return
    ismainfat = True
    for i in mainf.winfo_children():
        i.destroy()
    seqfr = Frame(mainf)
    seqtext = Text(seqfr, wrap=WORD, selectbackground="cyan")  # , yscrollincrement=20)
    seqtext.bind("<Return>", lambda *args: "break")
    seqtext.tag_config("tag_A", foreground="chocolate")
    seqtext.tag_config("tag_T", foreground="blueviolet")
    seqtext.tag_config("tag_C", foreground="darkgreen")
    seqtext.tag_config("tag_G", foreground="dodgerblue")

    def showseq(seq, seqtext, color=True, isupdate=False):
        global isdisplayseqcolored
        global cbar
        cbar.place(relwidth=0.8, relx=0.1)
        seqtext.config(state=NORMAL)
        seqtext.delete(0.0, END)
        root.update()
        if color:
            for i in range(len(seq)):
                try:
                    try:
                        seqtext.insert(END, seq[i], "tag_%s" % seq[i])
                    except Exception:
                        seqtext.insert(END, seq[i])
                    if i % 200 == 0:
                        cbar["value"] = int((i / len(seq)) * 100)
                        if isupdate:
                            root.update()
                except Exception:
                    return
        else:
            for i in range(len(seq)):
                try:
                    seqtext.insert(END, seq[i])
                    if i % 200 == 0:
                        cbar["value"] = int((i / len(seq)) * 100)
                        if isupdate:
                            root.update()
                except Exception:
                    return
        isdisplayseqcolored = color
        seqtext.config(state=DISABLED)
        cbar.place_forget()
        root.update()

    seqtextvbtf = ttk.Scrollbar(seqfr, orient=VERTICAL, command=seqtext.yview)
    seqtext.configure(yscrollcommand=seqtextvbtf.set)
    seqtextvbtf.pack(side=RIGHT, fill=Y)
    seqtext.pack(fill=BOTH, expand=1)
    seqfr.place(relheight=0.8, relwidth=1, relx=0, rely=0)

    root.update()

    def edcsq(*args):
        global editmode
        if editmode:
            return
        editmode = True
        seqtext.config(state=NORMAL)
        seqtext.delete(0.0, END)
        seqtext.insert(END, seqt)
        seqbut4.grid(row=1, column=4, padx=(10, 0), pady=10)
        # seqtext.config(state=DISABLED)

    def dene(*args):
        global isdisplayseqcolored
        global seqt
        global editmode
        seqbut4.grid_forget()
        seqt = (
            seqtext.get(0.0, END).replace(" ", "").replace("\n", "").replace("\r", "")
        )
        with open(os.path.join(projectpath, data["file"]), "w") as f:
            f.write(seqt)
        showseq(seqt, seqtext, isdisplayseqcolored)
        # seqtext.config(state=DISABLED)
        editmode = False

    def delleq(*args):
        global editmode
        global pjset
        global projectpath
        if editmode:
            return
        if messagebox.askyesno("AITD System", getlang("realdelseq")):
            if messagebox.askyesno("AITD System **AGAIN**", getlang("realdelseq")):
                treefile.delete(opened)
                os.remove(os.path.join(projectpath, data["file"]))
                os.remove(os.path.join(projectpath, data["metadata"]))
                for i in mainf.winfo_children():
                    i.destroy()
                del pjset["sequence_list"][opened]
                with open(os.path.join(projectpath, "setting.json"), "w") as f:
                    json.dump(pjset, f)

    def cuc(*args):
        global isdisplayseqcolored
        global seqt
        global editmode
        if editmode:
            return
        seqtext.config(state=NORMAL)
        if isdisplayseqcolored:
            isdisplayseqcolored = False
            seqtext.delete(0.0, END)
            seqtext.insert(END, seqt)
            # print("!")
        else:
            isdisplayseqcolored = True
            showseq(seqt, seqtext, isdisplayseqcolored)
            # print("!!")
        seqtext.config(state=DISABLED)

    secfr = Frame(mainf, bg="white")
    secfr.place(relheight=0.1, relwidth=1, relx=0, rely=0.8)

    global cbar
    cbar = ttk.Progressbar(secfr)

    if len(seqt) <= 5000:
        showseq(seqt, seqtext, True, True)
    else:
        showseq(seqt, seqtext, False, True)

    seqtext.config(state=DISABLED)

    global editmode
    editmode = False

    seqbut1 = ttk.Button(secfr, text=getlang("editseq"), command=edcsq)
    seqbut1.grid(row=1, column=1, padx=(10, 0), pady=10)
    seqbut2 = ttk.Button(secfr, text=getlang("occlr"), command=cuc)
    seqbut2.grid(row=1, column=2, padx=(10, 0), pady=10)
    seqbut3 = ttk.Button(secfr, text=getlang("deldeq"), command=delleq)
    seqbut3.grid(row=1, column=3, padx=(10, 0), pady=10)
    global seqbut4
    seqbut4 = ttk.Button(secfr, text=getlang("dene"), command=dene)
    secffr = Frame(mainf, bg="white")
    lbee1 = Text(secffr)
    lbee1.insert(
        END,
        "CODE: %s ; TYPE: %s . " % (opened, data["type"]),
    )
    if "description" in data:
        lbee1.insert(END, "DESCRIPTION: %s ; " % data["description"])
    if "from" in data:
        lbee1.insert(END, "FROM: %s ." % data["from"])
    lbee1.insert(END, "\nMETADATA: ")
    with open(os.path.join(projectpath, data["metadata"]), "r") as f:
        lbee1.pack(fill=BOTH, expand=1)
        lbee1.insert(END, f.read())
        lbee1.config(state=DISABLED)
    secffr.place(relheight=0.08, relwidth=1, relx=0, rely=0.9)
    root.update()


def importseq():
    global mainf
    global ismainfat
    global treefile
    global nowsthopen
    global impseq
    global projectpath
    global pjset
    global namespaces

    ismainfat = True

    def browse(*args):
        global openent
        file = filedialog.askopenfilename()
        if file:
            openent.config(state=NORMAL)
            openent.delete(0, END)
            openent.insert(END, file)
            openent.config(state=DISABLED)

    def openit(*args):
        global openent
        global parserchol
        global nowparser
        global treefile
        global impseq
        global getnumrer
        global nowsthopen
        global projectpath
        global mainf
        global pjset
        global namespaces
        lstlst = [aitd.Sequence() for i in range(int(getnumrer.get()))]
        if not isPlugin(nowparser.get().split("::")[0]):
            seeqtr = lambda data: getattr(aitd.xerlist.ParserList, nowparser.get())(
                data=data
            )
        else:
            zc_data = plugin_list[nowparser.get().split("::")[0]]["algorithm"][
                nowparser.get().split("::")[1]
            ]
            print(zc_data)
            seeqtr = eval(
                "lambda data: getattr(aitd.xerlist.ParserList, nowparser.get())(data=data,"
                + "".join(
                    ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                )
                + 'interaction=Interaction("%s"),iswindow=True)'
                % nowparser.get().split("::")[0]
            )
        aitd.readFile(openent.get(), seeqtr, lstlst)
        flag = True
        for i in range(len(lstlst)):
            if lstlst[i].sequence == "":
                if flag:
                    messagebox.showerror("AITD System", getlang("toomany"))
                    flag = False
                del lstlst[i]
        # previewnotest = ttk.Style()
        # previewnotest.configure("a.TNotebook",bg="white")
        # previewnotest.map("a.TNotebook", background= [("selected", "green")])
        s = ttk.Style()
        s.configure("Custom.TNotebook.Tab")
        s.map("Custom.TNotebook.Tab", foreground=[("selected", "red")])
        previewnote = ttk.Notebook(mainf, style="Custom.TNotebook")
        previewnote.place(relheight=0.6, relwidth=1, relx=0, rely=0.2)

        global nowsetsets
        nowsetsets = []
        global previewsetsetletents
        previewsetsetletents = []

        # def submitseq(code):
        #     global namespaces
        #     nasname = previewsetsetletents[code].get()
        #     setset = nowsetsets[code].get()
        #     if len(nasname.split("::")) != 2 or nasname in namespaces:
        #         messagebox.showerror("AITD System", getlang("errornamespacename"))
        #         return

        def submitseqs(*args):
            global namespaces
            global treefile
            global projectpath
            global nowsthopen
            global impseq
            global mainf
            global pjset
            for i in range(len(lstlst)):
                nasname = previewsetsetletents[i].get()
                if len(nasname.split("::")) != 2 or nasname in namespaces:
                    messagebox.showerror("AITD System", getlang("errornamespacename"))
                    return
            for i in range(len(lstlst)):
                nasname = previewsetsetletents[i].get()
                setset = nowsetsets[i].get()
                seqf = os.path.join(
                    "data", "sequence", "%s.seq" % (nasname.split("::")[1])
                )
                metf = os.path.join(
                    "data", "sequence", "%s.metadata" % (nasname.split("::")[1])
                )
                with open(os.path.join(projectpath, seqf), "w") as f:
                    f.write(lstlst[i].sequence)
                with open(os.path.join(projectpath, metf), "w") as f:
                    f.write(lstlst[i].metadata)
                # lstlst[i].sequence
                pjset["sequence_list"][nasname] = {
                    "file": seqf,
                    "name": nasname.split("::")[1],
                    "metadata": metf,
                    "type": setset,
                }
                namespaces[nasname] = pjset["sequence_list"][nasname]
                treefile.insert(
                    impseq, 1, nasname, text=pjset["sequence_list"][nasname]["name"]
                )
                with open(os.path.join(projectpath, "setting.json"), "w") as f:
                    json.dump(pjset, f)
            for i in mainf.winfo_children():
                i.destroy()
            nowsthopen = ""

        for i in range(len(lstlst)):
            previewframe = Frame(previewnote, bg="white")
            previewslab = Label(previewframe, text=getlang("previewslab"), bg="white")
            previewslab.place(x=5, rely=0)
            global previewstext
            previewstext = Text(previewframe, wrap=WORD)
            previewstext.place(relx=0, rely=0.07, relwidth=1, relheight=0.3)
            if len(lstlst[i].sequence) > 5000:
                previewstext.insert(END, lstlst[i].sequence[:4999] + "...")
            else:
                previewstext.insert(END, lstlst[i].sequence)
            previewstext.config(state=DISABLED)
            previewmlab = Label(previewframe, text=getlang("previewmlab"), bg="white")
            previewmlab.place(x=5, rely=0.38)
            global previewmtext
            previewmtext = Text(previewframe, wrap=WORD)
            previewmtext.place(relx=0, rely=0.45, relwidth=1, relheight=0.3)
            previewmtext.insert(END, lstlst[i].metadata)
            previewmtext.config(state=DISABLED)
            previewsetset = Label(
                previewframe, text=getlang("previewsetset"), bg="white"
            )
            previewsetset.place(x=5, rely=0.76)
            nowsetsets.append(StringVar())
            previewsetsetchol = ttk.Combobox(
                previewframe, state="readonly", textvariable=nowsetsets[i]
            )
            previewsetsetchol["values"] = ("gene", "genome", "protein", "transcript")
            previewsetsetchol.current(0)
            previewsetsetchol.place(x=125, rely=0.76, relwidth=0.4)
            # crlet = Frame(previewframe, bg="white")
            previewsetsetlet = Label(
                previewframe, text=getlang("previewsetsetlet"), bg="white"
            )
            previewsetsetlet.place(x=5, rely=0.86)
            previewsetsetletents.append(Entry(previewframe, bg="white"))
            previewsetsetletents[i].place(x=125, rely=0.86, relwidth=0.4)
            previewsetsetletents[i].insert(END, "seq::")
            # crlet.place(relx=0.5,rely=0.76)
            previewnote.add(previewframe, text="Seq %d" % (i + 1))

        previewendbut = ttk.Button(
            mainf,
            text=getlang("previewendbut"),
            command=submitseqs,
        )
        previewendbut.place(relx=0.8, rely=0.81, relwidth=0.15)

    openframe = Frame(mainf, bg="white")
    openframe.place(relheight=0.2, relwidth=1, relx=0, rely=0)
    openlab = Label(openframe, text=getlang("openwhich"), bg="white")
    openlab.place(x=5, y=10, relwidth=0.2)
    global openent
    openent = Entry(openframe)
    openent.place(relx=0.2, y=10, relwidth=0.55)
    openent.config(state=DISABLED)
    openbut = ttk.Button(openframe, text=getlang("browse"), command=browse)
    openbut.place(relx=0.8, y=10, relwidth=0.15)

    parserlab = Label(openframe, text=getlang("parserlab"), bg="white")
    parserlab.place(x=5, y=40, relwidth=0.2)
    global parserchol
    global nowparser
    nowparser = StringVar()
    parserchol = ttk.Combobox(openframe, state="readonly", textvariable=nowparser)
    parsercholl = []
    for i in aitd.xerlist.ParserList.__dict__:
        if len(i.split("::")) > 1:
            parsercholl.append(i)
    parserchol["values"] = tuple(parsercholl)
    parserchol.current(0)
    parserchol.place(relx=0.2, y=40, relwidth=0.55)

    getnumre = Label(openframe, text=getlang("getnumre"), bg="white")
    getnumre.place(x=5, y=70, relwidth=0.2)
    global getnumrer
    getnumrer = Spinbox(openframe, from_=1, to=1000)
    getnumrer.place(relx=0.2, y=70, relwidth=0.55)
    openbutt = ttk.Button(openframe, text=getlang("openit"), command=openit)
    openbutt.place(relx=0.8, y=70, relwidth=0.15)

    root.update()


def makealign():
    global pjset
    global mainf
    global projectpath
    global nowsthopen
    global comprr
    global namespaces
    openframe = Frame(mainf, bg="white")
    openframe.place(relheight=0.5, relwidth=1, relx=0, rely=0)

    seqs = []
    for i in pjset["sequence_list"]:
        seqs.append(i)

    aligncholl = []
    for i in aitd.xerlist.ComparatorList.__dict__:
        if len(i.split("::")) > 1:
            aligncholl.append(i)

    maxrncholl = []
    for i in aitd.xerlist.MatrixList.__dict__:
        if len(i.split("::")) > 1:
            maxrncholl.append(i)

    def startdo(*args):
        global seq1sv
        global seq2sv
        global cersv
        global pjset
        global mainf
        global maxsv
        global nowsthopen
        global namespaces
        global comprr
        global projectpath
        global gapcb
        if seq1sv.get() == seq2sv.get():
            messagebox.showerror("AITD System", getlang("sameseq"))
            return
        with open(
            os.path.join(projectpath, namespaces[seq1sv.get()]["file"]), "r"
        ) as f:
            seq1 = f.read()
        with open(
            os.path.join(projectpath, namespaces[seq2sv.get()]["file"]), "r"
        ) as f:
            seq2 = f.read()
        aliname = "ali::%s-%s" % (
            seq1sv.get().split("::")[-1],
            seq2sv.get().split("::")[-1],
        )
        if aliname in namespaces:
            if not messagebox.askyesno("AITD System", getlang("aliexi")):
                return
        willnamee = os.path.join(
            "data",
            "alignment",
            "%s.%s.ali" % (seq1sv.get().split("::")[-1], seq2sv.get().split("::")[-1]),
        )
        willname = os.path.join(projectpath, willnamee)
        # print(maxsv.get().split("::")[0])
        # print(plugin_list)
        if not isPlugin(maxsv.get().split("::")[0]):
            maxtr = lambda pos1, pos2: getattr(aitd.xerlist.MatrixList, maxsv.get())(
                pos1=pos1, pos2=pos2
            )
        else:
            zc_data = plugin_list[maxsv.get().split("::")[0]]["algorithm"][
                maxsv.get().split("::")[1]
            ]
            print(zc_data)
            maxtr = eval(
                "lambda  pos1, pos2: getattr(aitd.xerlist.MatrixList, maxsv.get())(pos1=pos1,pos2=pos2,"
                + "".join(
                    ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                )
                + 'interaction=Interaction("%s"),iswindow=True)'
                % maxsv.get().split("::")[0]
            )
            # maxtr = lambda pos1, pos2: getattr(aitd.xerlist.MatrixList, maxsv.get())(pos1=pos1,pos2=pos2)
        if not isPlugin(cersv.get().split("::")[0]):
            comtr = lambda seq1, seq2, maxfuc, gap: getattr(
                aitd.xerlist.ComparatorList, cersv.get()
            )(seq1=seq1, seq2=seq2, matrix=maxfuc, gap=gap)
        else:
            zc_data = plugin_list[cersv.get().split("::")[0]]["algorithm"][
                cersv.get().split("::")[1]
            ]
            print(zc_data)
            comtr = eval(
                "lambda  seq1, seq2, maxfuc, gap: getattr(aitd.xerlist.ComparatorList, cersv.get())(seq1=seq1,seq2=seq2,matrix=maxfuc,gap=gap,"
                + "".join(
                    ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                )
                + 'interaction=Interaction("%s"),iswindow=True)'
                % cersv.get().split("::")[0]
            )
        returns = comtr(seq1, seq2, maxtr, int(gapcb.get()))
        with open(willname + ".dat", "w") as f:
            f.write("%d\n%d" % (returns[0], returns[2]))
        acc1 = ""
        acc2 = ""
        for i in returns[1]:
            acc1 = acc1 + i[0]
            acc2 = acc2 + i[1]
        with open(willname, "w") as f:
            f.write("%s\n%s" % (acc1, acc2))
        alinam = {
            "file": willnamee,
            "opposing": [seq1sv.get(), seq2sv.get()],
            "data": willnamee + ".dat",
            "algorithm": cersv.get(),
            "matrix": maxsv.get(),
        }
        namespaces[aliname] = alinam
        pjset["alignment_list"][aliname] = alinam
        with open(os.path.join(projectpath, "setting.json"), "w") as f:
            json.dump(pjset, f)
        try:
            treefile.insert(
                comprr,
                1,
                aliname,
                text=aliname.split("::")[-1]
                + " -> "
                + pjset["alignment_list"][aliname]["algorithm"],
            )
        except Exception:
            pass
        messagebox.showinfo("AITD System", getlang("alisuc"))
        for i in mainf.winfo_children():
            i.destroy()
        nowsthopen = ""
        # waitinglabel = Label(root, text=getlang("plswat"), fg="black", bg="white")
        # waitinglabel.place(relx=0, rely=0, relwidth=1, relheight=1)
        # waitinglabel.config(alpha=0.5)
        # print(returns)

    seq1la = Label(openframe, text=getlang("seq1la"), bg="white")
    seq1la.place(x=5, y=10, relwidth=0.15)
    global seq1sv
    seq1sv = StringVar()
    seq1cb = ttk.Combobox(openframe, state="readonly", textvariable=seq1sv)
    seq1cb["values"] = tuple(seqs)
    seq1cb.current(0)
    seq1cb.place(relx=0.2, y=10, relwidth=0.55)

    seq2la = Label(openframe, text=getlang("seq2la"), bg="white")
    seq2la.place(x=5, y=40, relwidth=0.15)
    global seq2sv
    seq2sv = StringVar()
    seq2cb = ttk.Combobox(openframe, state="readonly", textvariable=seq2sv)
    seq2cb["values"] = tuple(seqs)
    seq2cb.current(0)
    seq2cb.place(relx=0.2, y=40, relwidth=0.55)

    cerla = Label(openframe, text=getlang("cerla"), bg="white")
    cerla.place(x=5, y=70, relwidth=0.15)
    global cersv
    cersv = StringVar()
    cercb = ttk.Combobox(openframe, state="readonly", textvariable=cersv)
    cercb["values"] = tuple(aligncholl)
    cercb.current(0)
    cercb.place(relx=0.2, y=70, relwidth=0.55)

    maxla = Label(openframe, text=getlang("maxla"), bg="white")
    maxla.place(x=5, y=100, relwidth=0.15)
    global maxsv
    maxsv = StringVar()
    maxcb = ttk.Combobox(openframe, state="readonly", textvariable=maxsv)
    maxcb["values"] = tuple(maxrncholl)
    maxcb.current(0)
    maxcb.place(relx=0.2, y=100, relwidth=0.55)

    gapla = Label(openframe, text=getlang("gapla"), bg="white")
    gapla.place(x=5, y=130, relwidth=0.15)
    global gapcb
    gapcb = Spinbox(openframe, from_=-100, to=100)
    gapcb.delete(0, END)
    gapcb.insert(END, -2)
    gapcb.place(relx=0.2, y=130, relwidth=0.55)

    # getnumre = Label(openframe, text=getlang("getnumre"), bg="white")
    # getnumre.place(x=5, y=70, relwidth=0.2)
    # global getnumrer
    # getnumrer = Spinbox(openframe, from_=1, to=1000)
    # getnumrer.place(relx=0.2, y=70, relwidth=0.55)
    openbutt = ttk.Button(openframe, text=getlang("startdo"), command=startdo)
    openbutt.place(relx=0.8, y=130, relwidth=0.15)


def maketree():
    global mainf
    global namespaces
    global nowsthopen
    global pjset
    global symbolchecked
    global symbolunchecked

    clblf = Frame(mainf, bg="white")

    clbl = Label(clblf, text=getlang("clbl"), bg="white")
    clbl.place(x=5)

    clblf.place(relwidth=1, relheight=0.05, relx=0, rely=0)

    colmainf = Frame(mainf)
    treetfile = ttk.Treeview(colmainf)
    treetfile.tag_configure("fggrey", foreground="grey")

    tvbtf = ttk.Scrollbar(colmainf, orient=VERTICAL, command=treetfile.yview)
    tvbtf.pack(side=RIGHT, fill=Y)
    tvbtfx = ttk.Scrollbar(colmainf, orient=HORIZONTAL, command=treetfile.xview)
    tvbtfx.pack(side=BOTTOM, fill=X)

    treetfile.config(yscrollcommand=tvbtf.set)
    treetfile.config(xscrollcommand=tvbtfx.set)

    # treetfile.heading(text=getlang("treetfileseq"))
    # treetfile.heading("abstract",text=getlang("treetfileab"))

    treetfile.tag_configure("checked", image=symbolchecked)
    treetfile.tag_configure("unchecked", image=symbolunchecked)

    def on_checkbox_changed(*args):
        item_id = treetfile.focus()
        checkbox_state = treetfile.item(item_id, "tag")
        if checkbox_state[0] == "checked":
            treetfile.item(item_id, tags=("unchecked",))
        else:
            treetfile.item(item_id, tags=("checked",))

    seqs, rs = [], 0
    for i in pjset["sequence_list"]:
        # with open(os.path.join(projectpath, pjset["sequence_list"][i]["file"])) as f:
        #     kseq = f.read()
        seqs.append(treetfile.insert("", 0, text=i, values=i))
        treetfile.item(seqs[rs], tags=("unchecked",))
        rs += 1

    # print(seqs)
    treetfile.bind("<<TreeviewSelect>>", on_checkbox_changed)

    treetfile.pack(fill=BOTH, expand=1)

    colmainf.place(relwidth=1, relheight=0.5, relx=0, rely=0.05)

    rcnxtf = Frame(mainf, bg="white")

    runins = [getlang("autoalign")]  # , getlang("saveautoalign")]

    global boxes
    boxes = []
    for i in range(len(runins)):
        boxes.append(BooleanVar())
        # boxes[i].set(True)
        cbt = Checkbutton(
            rcnxtf,
            text=runins[i],
            variable=boxes[i],
            bg="white",
            onvalue=True,
            offvalue=False,
        )
        cbt.grid(column=0, row=i, sticky=W)
        boxes[i].set(True)
        print(boxes[i].get())

    rcnxtf.place(relwidth=1, relheight=0.1, relx=0, rely=0.55)

    algorf = Frame(mainf, bg="white")

    Label(algorf, text=getlang("planter"), bg="white").place(x=5, y=0)

    aaligncholl = []
    for i in aitd.xerlist.TreePlanterList.__dict__:
        if len(i.split("::")) > 1:
            aaligncholl.append(i)

    global aseq1sv
    aseq1sv = StringVar()
    aseq1cb = ttk.Combobox(algorf, state="readonly", textvariable=aseq1sv)
    aseq1cb["values"] = tuple(aaligncholl)
    aseq1cb.current(0)
    aseq1cb.place(relx=0.2, y=0, relwidth=0.55)

    algorf.place(relwidth=1, relheight=0.05, relx=0, rely=0.65)

    def submittree(*args):
        global aseq1sv
        global pjset
        global nowsthopen
        global boxes
        global namespaces
        # for i in boxes:
        #     print(i.get())
        needmake = []
        for i in treetfile.get_children():
            if treetfile.item(i, "tag") == ("checked",):
                needmake.append(treetfile.item(i, "value")[0])
        ctneedmake = []
        for i in needmake:
            seqe = aitd.Sequence()
            with open(os.path.join(projectpath, namespaces[i]["file"]), "r") as f:
                seqe.sequence = f.read()
            with open(os.path.join(projectpath, namespaces[i]["metadata"]), "r") as f:
                seqe.metadata = f.read()
            seqe.type = namespaces[i]["type"]
            seqe.name = i
            ctneedmake.append(seqe)
        if len(needmake) < 3:
            messagebox.showwarning("AITD System", getlang("needmorethanthree"))
            return
        distances = [([0] * len(needmake)) for i in range(len(needmake))]
        for i in range(len(needmake) - 1):
            for j in range(i + 1, len(needmake)):
                seqreln1, seqreln2 = (
                    needmake[i].split("::")[1],
                    needmake[j].split("::")[1],
                )
                if ("ali::%s-%s" % (seqreln1, seqreln2) in namespaces) or (
                    "ali::%s-%s" % (seqreln2, seqreln1) in namespaces
                ):
                    try:
                        with open(
                            os.path.join(
                                projectpath,
                                namespaces["ali::%s-%s" % (seqreln1, seqreln2)]["data"],
                            ),
                            "r",
                        ) as f:
                            distances[i][j] = distances[j][i] = int(
                                f.read().splitlines()[1]
                            )
                    except Exception:
                        with open(
                            os.path.join(
                                projectpath,
                                namespaces["ali::%s-%s" % (seqreln2, seqreln1)]["data"],
                            ),
                            "r",
                        ) as f:
                            distances[i][j] = distances[j][i] = int(
                                f.read().splitlines()[1]
                            )
                elif not boxes[0].get():
                    messagebox.showwarning("AITD System", getlang("noali"))
                    return
                else:
                    with open(
                        os.path.join(projectpath, namespaces[needmake[i]]["file"]), "r"
                    ) as f:
                        seq1d = f.read()
                    with open(
                        os.path.join(projectpath, namespaces[needmake[j]]["file"]), "r"
                    ) as f:
                        seq2d = f.read()
                    if not isPlugin(defaultMatrix.split("::")[0]):
                        maxtr = lambda pos1, pos2: getattr(aitd.xerlist.MatrixList, defaultMatrix)(
                            pos1=pos1, pos2=pos2
                        )
                    else:
                        zc_data = plugin_list[defaultMatrix.split("::")[0]]["algorithm"][
                            defaultMatrix.split("::")[1]
                        ]
                        print(zc_data)
                        maxtr = eval(
                            "lambda  pos1, pos2: getattr(aitd.xerlist.MatrixList, defaultMatrix)(pos1=pos1,pos2=pos2,"
                            + "".join(
                                ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                            )
                            + 'interaction=Interaction("%s"),iswindow=True)'
                            % defaultMatrix.split("::")[0]
                        )
                    if not isPlugin(defaultComparator.split("::")[0]):
                        comtr = lambda seq1, seq2, maxfuc, gap: getattr(
                            aitd.xerlist.ComparatorList, defaultComparator
                        )(seq1=seq1, seq2=seq2, matrix=maxfuc, gap=gap)
                    else:
                        zc_data = plugin_list[defaultComparator.split("::")[0]]["algorithm"][
                            defaultComparator.split("::")[1]
                        ]
                        print(zc_data)
                        comtr = eval(
                            "lambda  seq1, seq2, maxfuc, gap: getattr(aitd.xerlist.ComparatorList, defaultComparator)(seq1=seq1,seq2=seq2,matrix=maxfuc,gap=gap,"
                            + "".join(
                                ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                            )
                            + 'interaction=Interaction("%s"),iswindow=True)'
                            % defaultComparator.split("::")[0]
                        )
                    aliadata = comtr(seq1d, seq2d, maxtr, defaultGap)
                    distances[i][j] = distances[j][i] = aliadata[2]
        # print(distances)
        if not isPlugin(aseq1sv.get().split("::")[0]):
            treetr = lambda seqs, distance: getattr(
                aitd.xerlist.TreePlanterList, aseq1sv.get()
            )(seqs=seqs, distance=distance)
        else:
            zc_data = plugin_list[aseq1sv.get().split("::")[0]]["algorithm"][
                aseq1sv.get().split("::")[1]
            ]
            print(zc_data)
            treetr = eval(
                "lambda seqs, distance: getattr(aitd.xerlist.TreePlanterList, aseq1sv.get())(seqs=seqs, distance=distance,"
                + "".join(
                    ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                )
                + 'interaction=Interaction("%s"),iswindow=True)'
                % aseq1sv.get().split("::")[0]
            )
        treedata = treetr(ctneedmake, distances)
        rccname = qccname = ""
        for i in ctneedmake:
            rccname = rccname + i.name.split("::")[1] + "-"
            qccname = qccname + i.name.split("::")[1] + "."
        rccname = rccname[:-1]
        qccname = qccname[:-1]
        treefilepath = os.path.join("data", "tree", qccname + ".tree")
        with open(os.path.join(projectpath, treefilepath), "wb") as f:
            pickle.dump(treedata, f)
        godata = {
            "file": treefilepath,
            "opposing": needmake,
            "algorithm": aseq1sv.get(),
        }
        namespaces["tree::" + rccname] = godata
        pjset["tree_list"]["tree::" + rccname] = godata
        with open(os.path.join(projectpath, "setting.json"), "w") as f:
            json.dump(pjset, f)
        messagebox.showinfo("AITD System", getlang("successmake"))
        try:
            treefile.insert(
                treestree,
                1,
                "tree::" + rccname,
                text=rccname
                + " -> "
                + pjset["tree_list"]["tree::" + rccname]["algorithm"],
            )
        except Exception:
            pass
        for i in mainf.winfo_children():
            i.destroy()
        nowsthopen = ""
        # print(treedata)

    buttf = Frame(mainf, bg="white")

    buttt = ttk.Button(buttf, text=getlang("submittree"), command=submittree)
    buttt.place(relx=0.8)

    buttf.place(relwidth=1, relheight=0.1, relx=0, rely=0.7)


def makesketch():
    global pjset
    global namespaces
    global nowsthopen
    global mainf
    openframe = Frame(mainf, bg="white")
    openframe.place(relheight=0.2, relwidth=1, relx=0, rely=0)

    parserlab = Label(openframe, text=getlang("seltre"), bg="white")
    parserlab.place(x=5, y=10, relwidth=0.2)
    global parsercholol
    global nowparserrer
    nowparserrer = StringVar()
    parsercholol = ttk.Combobox(openframe, state="readonly", textvariable=nowparserrer)
    parserchollll = []
    for i in pjset["tree_list"]:
        parserchollll.append(i)
    parsercholol["values"] = tuple(parserchollll)
    parsercholol.current(0)
    parsercholol.place(relx=0.2, y=10, relwidth=0.55)

    parserrlab = Label(openframe, text=getlang("displayer"), bg="white")
    parserrlab.place(x=5, y=40, relwidth=0.2)
    global wercholol
    global nowpaerrrer
    nowpaerrrer = StringVar()
    wercholol = ttk.Combobox(openframe, state="readonly", textvariable=nowpaerrrer)
    erh = []
    for i in aitd.xerlist.DisplayList.__dict__:
        if len(i.split("::")) > 1:
            erh.append(i)
    wercholol["values"] = tuple(erh)
    wercholol.current(0)
    wercholol.place(relx=0.2, y=40, relwidth=0.55)

    rcparserrlab = Label(openframe, text=getlang("typecc"), bg="white")
    rcparserrlab.place(x=5, y=70, relwidth=0.2)
    global rcwercholol
    global rcnowpaerrrer
    rcnowpaerrrer = StringVar()
    rcwercholol = ttk.Combobox(openframe, state="readonly", textvariable=rcnowpaerrrer)
    qerh = [".eps", ".png"]
    rcwercholol["values"] = tuple(qerh)
    rcwercholol.current(0)
    rcwercholol.place(relx=0.2, y=70, relwidth=0.55)

    def goforit(*args):
        global nowpaerrrer
        global mainf
        global nowsthopen
        global pjset
        global namespaces
        global nowparserrer
        global rcnowpaerrrer
        reer = nowpaerrrer.get()
        treee = nowparserrer.get()
        with open(os.path.join(projectpath, namespaces[treee]["file"]), "rb") as f:
            treedata = pickle.load(f)
        spacenamet = str(int(round(time.time() * 1000)))
        saveasname = os.path.join("cache", "sketch", spacenamet + rcnowpaerrrer.get())
        if not isPlugin(reer.split("::")[0]):
            distr = (
                lambda auxiliaryList, treeMark, n, display, isSave, savePath: getattr(
                    aitd.xerlist.DisplayList, reer
                )(
                    auxiliaryList=auxiliaryList,
                    treeMark=treeMark,
                    n=n,
                    display=display,
                    isSave=isSave,
                    savePath=savePath,
                )
            )
        else:
            zc_data = plugin_list[reer.split("::")[0]]["algorithm"][reer.split("::")[1]]
            print(zc_data)
            distr = eval(
                "lambda auxiliaryList, treeMark, n, display, isSave, savePath: getattr(aitd.xerlist.DisplayList, reer)(auxiliaryList=auxiliaryList, treeMark=treeMark, n=n, display=display, isSave=isSave, savePath=savePath,"
                + "".join(
                    ("%s=%s," % (i, getit(zc_data["args"][i]))) for i in zc_data["args"]
                )
                + 'interaction=Interaction("%s"),iswindow=True)' % reer.split("::")[0]
            )
        distr(
            treedata[0],
            treedata[1],
            len(namespaces[treee]["opposing"]) + 1,
            display=False,
            isSave=True,
            savePath=os.path.join(projectpath, saveasname),
        )
        foitdata = {
            "file": saveasname,
            "composition": namespaces[treee]["opposing"],
            "from": treee,
            "renderer": reer,
        }
        namespnam = "sketch::" + spacenamet
        namespaces[namespnam] = foitdata
        pjset["sketch_list"][namespnam] = foitdata
        with open(os.path.join(projectpath, "setting.json"), "w") as f:
            json.dump(pjset, f)
        messagebox.showinfo("AITD System", getlang("successmake"))
        for i in mainf.winfo_children():
            i.destroy()
        treefile.insert(
            treeske,
            1,
            namespnam,
            text=pjset["sketch_list"][namespnam]["from"] + " @ " + namespnam,
        )
        nowsthopen = ""

    openbutt = ttk.Button(openframe, text=getlang("startrn"), command=goforit)
    openbutt.place(relx=0.8, y=70, relwidth=0.15)

    root.update()


def vscsetting():
    global mainf
    global namespaces
    global pjset


def selection(*args, item=False):
    global nowsthopen
    global ismainfat
    global lists
    global namespaces
    # print(nowopen)
    if not nowopen:
        return
    if not item:
        try:
            item = treefile.selection()[0]
        except IndexError:
            return
    # print(item)
    canseb = ["seq", "sketch", "ali", "tree"]
    cansebb = ["rimpseq", "rcomprr", "rtreestree", "rsketch", "vscsetting"]
    if item:
        nowtype = item.split("::")[0]
        if (nowtype in canseb) or (item in cansebb):
            if nowsthopen == item:
                return
            nowsthopen = item
            if ismainfat:
                if not messagebox.askyesno("AITD System", getlang("reallyopen")):
                    return
            for i in mainf.winfo_children():
                i.destroy()
        else:
            return
        if len(item.split("::")) > 1:
            if nowtype == "seq":
                displayseq(namespaces[item], item)
            elif nowtype == "sketch":
                displaysktch(namespaces[item], item)
            elif nowtype == "ali":
                displayali(namespaces[item], item)
            elif nowtype == "tree":
                displaytree(namespaces[item], item)
        else:
            if item == "rimpseq":
                importseq()
            elif item == "rcomprr":
                makealign()
            elif item == "rtreestree":
                maketree()
            elif item == "rsketch":
                makesketch()
            elif item == "vscsetting":
                vscsetting()
        for i in plugin_list:
            zc_data = plugin_list[i]
            if zc_data["refresh"]["open"]:
                exec(
                    "import plugins.%s.%s"
                    % (zc_data["name"], zc_data["refresh"]["file"])
                )
                exec(
                    "plugins.%s.%s.%s("
                    % (
                        zc_data["name"],
                        zc_data["refresh"]["file"],
                        zc_data["refresh"]["prototype"],
                    )
                    + "".join(
                        ("%s=%s," % (i, getit(zc_data["refresh"]["args"][i])))
                        for i in zc_data["refresh"]["args"]
                    )
                    + 'interaction=Interaction("%s"),iswindow=True)' % zc_data["name"],
                )


openseqbut = ttk.Button(
    sidef,
    text=getlang("openseqbut"),
    command=lambda *args: selection(*args, item="rimpseq"),
)
openseqbut.place(rely=0.81, relx=0.05, relwidth=0.4)
plibut = ttk.Button(
    sidef, text=getlang("plibut"), command=lambda *args: selection(*args, item="pict")
)
plibut.place(rely=0.81, relx=0.55, relwidth=0.4)
makealib = ttk.Button(
    sidef,
    text=getlang("makealib"),
    command=lambda *args: selection(*args, item="rcomprr"),
)
makealib.place(rely=0.86, relx=0.05, relwidth=0.4)
gototre = ttk.Button(
    sidef,
    text=getlang("gototre"),
    command=lambda *args: selection(*args, item="rtreestree"),
)
gototre.place(rely=0.86, relx=0.55, relwidth=0.4)
gotosre = ttk.Button(
    sidef,
    text=getlang("gotosre"),
    command=lambda *args: selection(*args, item="rsketch"),
)
gotosre.place(rely=0.91, relx=0.05, relwidth=0.4)

treefile.bind("<ButtonRelease-1>", selection)


def mkdir(path):
    # Renote("%s %s..." % (getword("createdict"), path), end=" ")
    try:
        os.makedirs(path)
    except Exception:
        pass


def mkfile(filename, mode="w"):
    # Renote("%s %s..." % (getword("createfile"), filename), end=" ")
    try:
        open(filename, "w").close()
        # print(getword("done"))
        return True
    except Exception:
        # print()
        messagebox.showerror(
            "AITD System", "%s : %s" % (getlang("filenotcreate"), filename)
        )
        return False


def openpj(*args, pp=""):
    global projectpath
    global nowopen
    global pjset
    global root
    global namespaces
    if nowopen:
        if not messagebox.askyesno("AITD System", getlang("hasopened")):
            return
    nowopen = False
    treefile.delete(*treefile.get_children())
    for i in mainf.winfo_children():
        i.destroy()
    if pp == "":
        print(pp)
        projectpath = os.path.abspath(
            os.path.join(
                filedialog.askopenfilename(
                    title="AITD System",
                    filetypes=(("Project Setting", "setting.json"),),
                ),
                os.pardir,
            )
        )
        # projectpath = filedialog.askdirectory(title=getlang("openpj"),initialdir="C:\\")
        if not os.path.exists(projectpath):
            messagebox.showerror("AITD System", getlang("notfoundpj"))
            return
    else:
        projectpath = pp
    if not os.path.exists(os.path.join(projectpath, "setting.json")):
        messagebox.showerror("AITD System", getlang("notfoundpj"))
        return
    with open(os.path.join(projectpath, "setting.json"), "r") as f:
        pjset = json.load(f)
    global pjsetting, vscsetting, impseq, impty, treeske, smpty, treestree, tmpty, aicr, osjr, artd, esep, pict, pmpty, comprr
    # symbolplugin
    pict = treefile.insert("", 0, "pict", text=getlang("pict"), image=symbolplugin)
    # pmpty = treefile.insert(
    #     pict,
    #     1,
    #     "pmpty",
    #     text=getlang("pmpty"),
    #     value=f"{pict}-{getlang('pmpty')}",
    #     tags=("fggrey"),
    # )
    aicr = treefile.insert("", 0, "aicr", text=getlang("aicr"), image=symbolcomputer)
    osjr = treefile.insert(
        aicr, 1, "osjr", text=getlang("osjr"), value=f"{aicr}-{getlang('osjr')}"
    )
    artd = treefile.insert(
        aicr, 1, "artd", text=getlang("artd"), value=f"{aicr}-{getlang('artd')}"
    )
    esep = treefile.insert(
        aicr, 1, "esep", text=getlang("esep"), value=f"{aicr}-{getlang('esep')}"
    )
    treestree = treefile.insert(
        "", 0, "treestree", text=getlang("treestree"), image=symboltree
    )
    # tmpty = treefile.insert(
    #     treestree,
    #     1,
    #     "tmpty",
    #     text=getlang("impty"),
    #     value=f"{treestree}-{getlang('impty')}",
    #     tags=("fggrey"),
    # )
    treeske = treefile.insert(
        "", 0, "treeske", text=getlang("treeske"), image=symbolsketch
    )
    # smpty = treefile.insert(
    #     treeske,
    #     1,
    #     "smpty",
    #     text=getlang("impty"),
    #     value=f"{treeske}-{getlang('impty')}",
    #     tags=("fggrey"),
    # )
    comprr = treefile.insert(
        "", 0, "comprr", text=getlang("comprr"), image=symbolsearch
    )
    impseq = treefile.insert("", 0, "impseq", text=getlang("impseq"), image=symbolDNA)
    # impty = treefile.insert(
    #     impseq,
    #     1,
    #     "impty",
    #     text=getlang("impty"),
    #     value=f"{impseq}-{getlang('impty')}",
    #     tags=("fggrey"),
    # )
    pjsetting = treefile.insert(
        "", 0, "pjsetting", text=getlang("pjsetting"), image=symbolsetting
    )
    vscsetting = treefile.insert(
        pjsetting,
        1,
        "vscsetting",
        text=getlang("vscsetting"),
        value=f"{pjsetting}-{getlang('vscsetting')}",
    )

    root.update()

    nowopen = True

    for i in pjset:
        if i in ["sequence_list", "tree_list", "sketch_list", "alignment_list"]:
            for j in pjset[i]:
                namespaces[j] = pjset[i][j]

    for i in pjset["sequence_list"]:
        treefile.insert(impseq, 1, i, text=pjset["sequence_list"][i]["name"])

    for i in pjset["alignment_list"]:
        treefile.insert(
            comprr,
            1,
            i,
            text=i.split("::")[-1] + " -> " + pjset["alignment_list"][i]["algorithm"],
        )

    for i in pjset["tree_list"]:
        treefile.insert(
            treestree,
            1,
            i,
            text=i.split("::")[-1] + " -> " + pjset["tree_list"][i]["algorithm"],
        )

    for i in pjset["sketch_list"]:
        treefile.insert(treeske, 1, i, text=pjset["sketch_list"][i]["from"] + " @ " + i)
    # print(pjset)


def newpj(*args):
    projectwill = os.path.abspath(
        os.path.join(
            filedialog.asksaveasfilename(
                title="AITD System",
                filetypes=[
                    ("Project Setting", "setting.json"),
                ],
                defaultextension="setting.json",
            ),
            os.pardir,
        )
    )
    mkdir(projectwill)
    mkdir(os.path.join(projectwill, "input"))
    mkdir(os.path.join(projectwill, "plugins"))
    mkfile(os.path.join(projectwill, "plugins", "plugin_list.dat"))
    mkdir(os.path.join(projectwill, "data"))
    mkdir(os.path.join(projectwill, "data", "sequence"))
    mkdir(os.path.join(projectwill, "data", "alignment"))
    mkdir(os.path.join(projectwill, "data", "tree"))
    mkdir(os.path.join(projectwill, "data", "correction"))
    mkdir(os.path.join(projectwill, "training"))
    mkdir(os.path.join(projectwill, "output"))
    mkdir(os.path.join(projectwill, "cache"))
    mkdir(os.path.join(projectwill, "cache", "sketch"))
    mkdir(os.path.join(projectwill, "cache", "log"))
    mkfile(os.path.join(projectwill, "setting.json"))
    with open(os.path.join(projectwill, "setting.json"), "w") as f:
        json.dump(
            {
                "name": os.path.basename(projectwill),
                "sequence_list": {},
                "alignment_list": {},
                "tree_list": {},
                "sketch_list": {},
            },
            f,
        )
    mkfile(os.path.join(projectwill, "setting.dat"))
    openpj(pp=projectwill)


def abouabout(*args):
    aboutpage = Toplevel(root)
    aboutpage.geometry("450x350")
    aboutpage.configure(bg="white")
    aboutpage.resizable(False, False)
    Label(
        aboutpage, text="AITD System", bg="white", font=("思源黑体 Normal", 25)
    ).pack()
    Label(
        aboutpage,
        text="""Copyright 2024 Zhu jingrui, Hu Gaoyuan, Deng Yutong, et al

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""",
        bg="white",
        font=("思源黑体 Normal", 8),
        justify="left",
    ).pack()
    Label(
        aboutpage,
        text="To see licenses for other works used in this project, please check .\\licenses\\ !",
        font=("思源黑体 Normal", 8),
        bg="white",
        fg="red",
    ).pack()


menu = tkinter.Menu(root)

filesubmenu = tkinter.Menu(menu, tearoff=0)
filesubmenu.add_command(label=getlang("newpj"), accelerator="Ctrl+N", command=newpj)
filesubmenu.add_command(label=getlang("openpj"), accelerator="Ctrl+O", command=openpj)

# rcopenpjnemu = tkinter.Menu(filesubmenu, tearoff=0)
# rcopenpjnemu.add_command(label=getlang("norcpj"), accelerator="Ctrl+Shift+D")
# rcopenpjnemu.add_separator()
# filesubmenu.add_cascade(label=getlang("rcpj"), menu=rcopenpjnemu)

# filesubmenu.add_separator()
# filesubmenu.add_command(label=getlang("openseq"), accelerator="Ctrl+Shift+O")
# filesubmenu.add_command(label=getlang("opencom"), accelerator="Ctrl+Alt+O")
# filesubmenu.add_separator()
# filesubmenu.add_command(label=getlang("copypj"), accelerator="Ctrl+Shift+S")
filesubmenu.add_separator()
filesubmenu.add_command(label=getlang("setting"), accelerator="Ctrl+S")


helpsubmenu = tkinter.Menu(menu, tearoff=0)
helpsubmenu.add_command(
    label=getlang("about_about"), accelerator="Ctrl+H", command=abouabout
)
helpsubmenu.add_command(label=getlang("helpdoc"), accelerator="Ctrl+D")

menu.add_cascade(label=getlang("file"), menu=filesubmenu)
menu.add_cascade(label=getlang("help"), menu=helpsubmenu)


root.config(menu=menu)

root.bind("<Control-o>", openpj)
root.bind("<Control-h>", abouabout)
# root.bind("<Control-Shift-s>",copypj)
# root.bind("<Control-Shift-o>",lambda *args: selection(*args, item="pict"))

openpj(pp="C:\\Users\\87023\\OneDrive\\科创大赛\\AITD System\\test")

root.mainloop()
