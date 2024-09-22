with open(os.path.join(projectpath, "setting.json"), "r") as f:
pjset = json.load(f)

for i in pjset:
    if i in ["sequence_list", "tree_list", "sketch_list", "alignment_list"]:
        for j in pjset[i]:
            namespaces[j] = pjset[i][j]