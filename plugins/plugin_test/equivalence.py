import os

def main(pos1, pos2, interaction, iswindow, inPlugin, dir, isOutputDir):
    if not inPlugin:
        interaction.Error("Running outside of the plugin!")
    if isOutputDir:
        print(os.path.join(dir, "setting.json"))
    return pos1 == pos2
