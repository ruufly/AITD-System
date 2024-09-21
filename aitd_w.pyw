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

root = Tk(className="AITD_System")
root.title("AITD System")
root.configure(background="white")
root.update()
scx, scy = root.winfo_screenwidth(), root.winfo_screenheight()
wdx, wdy = root.winfo_width(), root.winfo_height()
root.minsize(int(scx / 2), int(scy / 1.6))
# root.maxsize(int(scx / 2), int(scy / 1.8))

programdict = os.path.dirname(os.path.abspath(__file__))

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

with open(os.path.join(programdict, "data", "setting.dat"), "rb") as f:
    try:
        config = pickle.load(f)
    except EOFError:
        config = {"language": "en"}
        with open(os.path.join(programdict, "data", "setting.dat"), "wb") as f:
            pickle.dump(config, f)

with open(os.path.join(programdict, "data", "en.yml"), "r", encoding="utf-8") as f:
    endata = yaml.safe_load(f.read())

langdata = endata


def getlang(word):
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

# for i in range(20): treefile.insert("",0,str(i),text=str(i))


def displaysktch(data, opened):
    global projectpath
    global sktchphoto
    global ismainfat
    ismainfat = False
    sktchphoto = ImageTk.PhotoImage(Image.open(os.path.join(projectpath, data["file"])))
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
    ismainfat = True


def displayseq(data, opened):
    # global nowsthopen
    global ismainfat
    global projectpath
    global isdisplayseqcolored
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
    seqtext = Text(seqfr, wrap=WORD, selectbackground="cyan")
    seqtext.bind("<Return>", lambda *args: "break")
    seqtext.tag_config("tag_A", foreground="chocolate")
    seqtext.tag_config("tag_T", foreground="red")
    seqtext.tag_config("tag_C", foreground="darkgreen")
    seqtext.tag_config("tag_G", foreground="blue")

    def showseq(seq, seqtext, color=True):
        global isdisplayseqcolored
        seqtext.delete(0.0, END)
        if color:
            for i in range(len(seq)):
                try:
                    if seq[i] == "A":
                        seqtext.insert(END, seq[i], "tag_A")
                    elif seq[i] == "C":
                        seqtext.insert(END, seq[i], "tag_C")
                    elif seq[i] == "G":
                        seqtext.insert(END, seq[i], "tag_G")
                    elif seq[i] == "T":
                        seqtext.insert(END, seq[i], "tag_T")
                    else:
                        seqtext.insert(END, seq[i])
                    if i % 100 == 0:
                        root.update()
                except Exception:
                    return
        else:
            for i in range(len(seq)):
                try:
                    seqtext.insert(END, seq[i])
                    if i % 100 == 0:
                        root.update()
                except Exception:
                    return
        isdisplayseqcolored = color

    seqtextvbtf = ttk.Scrollbar(seqfr, orient=VERTICAL, command=seqtext.yview)
    seqtext.configure(yscrollcommand=seqtextvbtf.set)
    seqtextvbtf.pack(side=RIGHT, fill=Y)
    seqtext.pack(fill=BOTH, expand=1)
    seqfr.place(relheight=0.8, relwidth=1, relx=0, rely=0)

    root.update()

    if len(seqt) <= 5000:
        showseq(seqt, seqtext, True)
    else:
        showseq(seqt, seqtext, False)

    seqtext.config(state=DISABLED)

    global editmode
    editmode = False

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
        seqtext.config(state=DISABLED)
        editmode = False

    def delleq(*args):
        global editmode
        if editmode:
            return
        if messagebox.askyesno("AITD System", getlang("realdelseq")):
            if messagebox.askyesno("AITD System **AGAIN**", getlang("realdelseq")):
                treefile.delete(opened)
                os.remove(os.path.join(projectpath, data["file"]))
                os.remove(os.path.join(projectpath, data["metadata"]))
                for i in mainf.winfo_children():
                    i.destroy()

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
            print("!")
        else:
            isdisplayseqcolored = True
            showseq(seqt, seqtext, isdisplayseqcolored)
            print("!!")
        seqtext.config(state=DISABLED)

    secfr = Frame(mainf, bg="white")
    seqbut1 = ttk.Button(secfr, text=getlang("editseq"), command=edcsq)
    seqbut1.grid(row=1, column=1, padx=(10, 0), pady=10)
    seqbut2 = ttk.Button(secfr, text=getlang("occlr"), command=cuc)
    seqbut2.grid(row=1, column=2, padx=(10, 0), pady=10)
    seqbut3 = ttk.Button(secfr, text=getlang("deldeq"), command=delleq)
    seqbut3.grid(row=1, column=3, padx=(10, 0), pady=10)
    global seqbut4
    seqbut4 = ttk.Button(secfr, text=getlang("dene"), command=dene)
    secfr.place(relheight=0.1, relwidth=1, relx=0, rely=0.8)
    secffr = Frame(mainf, bg="white")
    lbee1 = Text(secffr)
    lbee1.insert(
        END,
        "CODE: %s ; TYPE: %s; DESCRIPTION: %s ; FROM: %s .\nMETADATA: "
        % (opened, data["type"], data["description"], data["from"]),
    )
    with open(os.path.join(projectpath, data["metadata"]), "r") as f:
        lbee1.pack(fill=BOTH, expand=1)
        lbee1.insert(END, f.read())
        lbee1.config(state=DISABLED)
    secffr.place(relheight=0.08, relwidth=1, relx=0, rely=0.9)


def selection(*args):
    global nowsthopen
    global ismainfat
    try:
        item = treefile.selection()[0]
    except IndexError:
        return
    # print(item)
    if item:
        if len(item.split("::")) > 1:
            if nowsthopen == item:
                return
            nowsthopen = item
            if ismainfat:
                if not messagebox.askyesno("AITD System", getlang("reallyopen")):
                    return
            for i in mainf.winfo_children():
                i.destroy()
            nowtype = item.split("::")[0]
            if nowtype == "seq":
                displayseq(namespaces[item], item)
            elif nowtype == "sktch":
                displaysktch(namespaces[item], item)
            elif nowtype == "ali":
                displayali(namespaces[item], item)
        else:
            ...


treefile.bind("<ButtonRelease-1>", selection)


def openpj(*args, pp=""):
    global projectpath
    global nowopen
    global pjset
    global namespaces
    if nowopen:
        if not messagebox.askyesno("AITD System", getlang("hasopened")):
            return
    if not pp:
        projectpath = filedialog.askdirectory(title=getlang("openpj"))
        if not os.path.exists(projectpath):
            messagebox.showerror("AITD System", getlang("notfoundpj"))
            return
    else:
        projectpath = pp
    nowopen = True
    treefile.delete(*treefile.get_children())
    global pjsetting, vscsetting, impseq, impty, treeske, smpty, treestree, tmpty, aicr, osjr, artd, esep, pict, pmpty
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

    with open(os.path.join(projectpath, "setting.json"), "r") as f:
        pjset = json.load(f)

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
            text=i.split("::")[-1]
            + " -> "
            + pjset["tree_list"][i]["algorithm"]
            + " & "
            + pjset["tree_list"][i]["processor"],
        )

    for i in pjset["sketch_list"]:
        treefile.insert(treeske, 1, i, text=pjset["sketch_list"][i]["from"] + " @ " + i)
    print(pjset)


menu = tkinter.Menu(root)

filesubmenu = tkinter.Menu(menu, tearoff=0)
filesubmenu.add_command(label=getlang("newpj"), accelerator="Ctrl+N")
filesubmenu.add_command(label=getlang("openpj"), accelerator="Ctrl+O", command=openpj)

# rcopenpjnemu = tkinter.Menu(filesubmenu, tearoff=0)
# rcopenpjnemu.add_command(label=getlang("norcpj"), accelerator="Ctrl+Shift+D")
# rcopenpjnemu.add_separator()
# filesubmenu.add_cascade(label=getlang("rcpj"), menu=rcopenpjnemu)

filesubmenu.add_separator()
filesubmenu.add_command(label=getlang("openseq"), accelerator="Ctrl+Shift+O")
filesubmenu.add_command(label=getlang("opencom"), accelerator="Ctrl+Alt+O")
filesubmenu.add_separator()
filesubmenu.add_command(label=getlang("copypj"), accelerator="Ctrl+Shift+S")
filesubmenu.add_separator()
filesubmenu.add_command(label=getlang("setting"), accelerator="Ctrl+,")


helpsubmenu = tkinter.Menu(menu, tearoff=0)
helpsubmenu.add_command(label=getlang("about_about"), accelerator="Ctrl+H")
helpsubmenu.add_command(label=getlang("helpdoc"), accelerator="Ctrl+D")

menu.add_cascade(label=getlang("file"), menu=filesubmenu)
menu.add_cascade(label=getlang("help"), menu=helpsubmenu)


root.config(menu=menu)

openpj(pp="C:\\Users\\87023\\OneDrive\\科创大赛\\AITD System\\test")

root.mainloop()
