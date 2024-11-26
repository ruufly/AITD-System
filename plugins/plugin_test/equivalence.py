import os

def main(pos1, pos2, interaction, iswindow, inPlugin, isOutputDir):
    if not inPlugin:
        interaction.Error("Running outside of the plugin!")
    if isOutputDir == "true":
        interaction.Note("setting.json")
    return pos1 == pos2
