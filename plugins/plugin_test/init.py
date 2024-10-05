def makecolor(master, color):
    try:
        master.config(bg=color)
    except Exception:
        pass
    for i in master.winfo_children():
        makecolor(i, color)


def main(interaction, iswindow, mainf, topf, sidef, root, color):
    # interaction.Note("You has installed the plugin named \"plugin_test\" and have fun!")
    if iswindow:
        makecolor(mainf,color)
        makecolor(topf,color)
        makecolor(sidef,color)
        root.update()