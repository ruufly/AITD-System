def makecolor(master, color):
    try:
        master.config(bg=color)
    except Exception:
        pass
    for i in master.winfo_children():
        makecolor(i, color)


def main(interaction, iswindow, mainf, topf, sidef, root, color):
    if iswindow:
        makecolor(mainf,color)
        makecolor(topf,color)
        makecolor(sidef,color)
        root.update()
