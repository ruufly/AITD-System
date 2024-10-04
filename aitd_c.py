import os, sys
import aitd
import json
import pickle
import yaml
import zipfile
from colorama import Fore, Back, Style

argv = sys.argv

programdict = os.path.dirname(os.path.abspath(__file__))


####################
# I'M HERE!!!      #
####################
# 以下为所需的接口

def treeModel():
    pass

def getName(name):  # 获得程序生成的唯一名称
    pass

SpeciesList = [...] # 用于存储已经创建的物种
SeqMap = {"":[...]} # 用于将序列和物种一一对应

def saveSetting(projectDict):
    with open(projectDict + "setting.json") as setting:
        settingData = json.load(setting)
        for species in SpeciesList:
            for seq in SeqMap[species]:
                settingData["sequence_list"]["seq::" + seq] = species
                
def getNamespace(namespace): # 用于获取命名空间名所在位置
    pass

def getObject(str):
    with open(programdict + "setting.json") as js:
        contents = json.read(js)
        
#endif  // 乱入

helps = """
+-----------------------------------------------------------------+
|                          AITD System                            |
|  A systematic phylogenetic tree drawing and species evolution   |
|                 path inference system based on                  |
|         specific macromolecular sequence alignment and          |
|            automatic sequence screening techniques.             |
+=================================================================+
| Commands """ + Style.BRIGHT + "(Normal Mode)" + Style.RESET_ALL + """                                          |
+-----------------+-----------------------------------------------+
| setting         | setting <option> <value>                      |
| new             | new <type> <name> [<parameter>]               |
| open            | open [<name>]                                 |
| debug           | debug [on|off]                                |
| exit            |                                               |
+=================+===============================================+
| Commands """ + Fore.CYAN + "(Debug mode)" + Style.RESET_ALL + """                                           |
+-----------------------------------------------------------------+
| (You can directly run a single line of Python code)             |
+=================================================================+
| Commands """ + Fore.MAGENTA + "(Project Mode)" + Style.RESET_ALL + """                                         |
+-----------------+-----------------------------------------------+
|                 |                                               |
+=================+===============================================+
| Welcome to AITD System!                                         |
+-----------------------------------------------------------------+
"""


def Fatal(message):
    print(
        Style.BRIGHT + Fore.WHITE + Back.RED + "[Fatal] %s" % message + Style.RESET_ALL
    )


def Error(message):
    print(Fore.RED + "[Error] %s" % message + Style.RESET_ALL)


def Warning(message):
    print(Fore.YELLOW + "[Warning] %s" % message + Style.RESET_ALL)


def Note(message):
    print(Fore.CYAN + "[Note] %s" % message + Style.RESET_ALL)


def reNote(message, end):
    print("       %s" % message, end=end)


with open(os.path.join(programdict, "data", "setting.dat"), "rb") as f:
    try:
        config = pickle.load(f)
    except EOFError:
        config = {"language": "en"}
        with open(os.path.join(programdict, "data", "setting.dat"), "wb") as f:
            pickle.dump(config, f)

with open(os.path.join(programdict, "data", "en.yml"), "r", encoding="utf-8") as f:
    EnData = yaml.safe_load(f.read())

langData = EnData


def getWord(word):
    if word in langData:
        return langData[word]
    elif word in EnData:
        return EnData[word]
    else:
        Fatal("Unable to find corresponding language information: %s" % word)
        exit(-1)


def refresh_setting():
    global langData
    try:
        with open(
            os.path.join(programdict, "data", "%s.yml" % config["language"]),
            "r",
            encoding="utf-8",
        ) as f:
            langData = yaml.safe_load(f.read())
    except Exception as e:
        Fatal("Unable to load language file: %s.yml" % (config["language"]))
        langData = EnData
        return False
    return True


refresh_setting()


def mkdir(path):
    reNote("%s %s..." % (getWord("createdict"), path), end=" ")
    try:
        os.makedirs(path)
        print("done.")
        return True
    except Exception:
        print()
        Error("%s : %s" % (getWord("dictnotcreate"), path))
        return False


def mkfile(filename, mode="w"):
    reNote("%s %s..." % (getWord("createfile"), filename), end=" ")
    try:
        open(filename, "w").close()
        print(getWord("done"))
        return True
    except Exception:
        print()
        Error("%s : %s" % (getWord("filenotcreate"), filename))
        return False


print(helps)

nowProject = ""
debug = False

while True:
    if nowProject == "":
        ouInput = 'AITD "%s"> ' % os.getcwd()
    else:
        ouInput = (
            'AITD "%s" ' % os.getcwd()
            + Fore.MAGENTA
            + 'with the project "%s"' % nowProject
            + Style.RESET_ALL
            + ">"
        )
    if debug:
        ouInput = Fore.CYAN + "[DEBUG] " + Style.RESET_ALL + ouInput
    oriInput = input(ouInput)
    command = oriInput.split()
    if len(command) == 0:
        continue
    elif command[0] == "clear":
        os.system("cls")
    elif command[0] == "setting":
        if len(command) < 3:
            Error(getWord("synerr"))
            Note("%s : setting <option> <value>" % getWord("usage"))
            continue
        if command[1] == "language":
            config["language"] = command[2]
            with open("data/setting.dat", "wb") as f:
                pickle.dump(config, f)
            if refresh_setting():
                Note("%s %s" % (getWord("langset"), config["language"]))
        else:
            Error(getWord("notsetting"))
    elif command[0] == "new":
        if len(command) < 3:
            Error(getWord("synerr"))
            Note("%s : new <type> <name> [<parameter>]" % getWord("usage"))
            continue
        if command[1] == "project":
            Note(getWord("mkpj"))
            mkdir(command[2])
            mkdir(os.path.join(command[2], "input"))
            mkdir(os.path.join(command[2], "plugins"))
            mkfile(os.path.join(command[2], "plugins", "plugin_list.dat"))
            mkdir(os.path.join(command[2], "data"))
            mkdir(os.path.join(command[2], "data", "sequence"))
            mkdir(os.path.join(command[2], "data", "alignment"))
            mkdir(os.path.join(command[2], "data", "tree"))
            mkdir(os.path.join(command[2], "data", "correction"))
            mkdir(os.path.join(command[2], "training"))
            mkdir(os.path.join(command[2], "output"))
            mkdir(os.path.join(command[2], "cache"))
            mkdir(os.path.join(command[2], "cache", "sketch"))
            mkdir(os.path.join(command[2], "cache", "log"))
            mkfile(os.path.join(command[2], "setting.json"))
            with open(os.path.join(command[2], "setting.json"), "w") as f:
                json.dump({}, f)
            mkfile(os.path.join(command[2], "setting.dat"))
            Note(getWord("pjcreated"))
        else:
            Error(getWord("synerr"))
            Note("%s : new <type> <name> [<parameter>]" % getWord("usage"))
            continue
    elif command[0] == "open":
        if len(command) == 2:
            try:
                os.chdir(os.path.join(os.getcwd(), command[1]))
                nowProject = command[1]
            except FileNotFoundError:
                Error(getWord("notpjdict"))
                nowProject = ""
                continue
        else:
            nowProject = os.path.split(os.getcwd())[1]
        # try:
        #     nowProject = command[1]
        # except IndexError:
        #     Error(getWord("synerr"))
        #     Note("%s : open <name>" % getWord("usage"))
        #     continue
        try:
            with open(os.path.join("setting.json"), "r") as f:
                if json.load(f) == {}:
                    Warning(getWord("warnbasic"))
        except Exception:
            Error(getWord("wpj"))
            nowProject = ""
            continue
    elif command[0] == "debug":
        if len(command) == 1 or command[1] == "on":
            debug = True
        elif command[1] == "off":
            debug = False
        else:
            Error(getWord("synerr"))
            Note("%s : debug [on|off]" % getWord("usage"))
            continue
    elif command[0] == "exit":
        if nowProject != "":
            Note(getWord("exitpj"))
            os.chdir(os.path.join(os.getcwd(), ".."))
            nowProject = ""
        else:
            Note(getWord("exit"))
            print(
            """
+-----------------------------------------------------------------+
|                          AITD System                            |
|               Welcome to use this software again!               |
+=================================================================+
| Staff                                                           |
+------------------------------+----------------------------------+
| Zhu Jingrui (distjr_)        |  who built the overall project   |
|                              |    and wrote most of the code    |
+------------------------------+----------------------------------+
| Hu Gaoyuan (hzzzzzzzzzzzzz)  |      who proposed several        |
|                              |         key algorithms           |
+------------------------------+----------------------------------+
| Deng Yutong (dyt_dirt)       |    who conducted AI training     |
|                              |       and wrote some code        |
+==============================+==================================+
| Credits                                                         |
+------------------------------+----------------------------------+
| Bai Zhiyuan (Qemu_Android)   |   who provided the necessary     |
|                              | computing power for training AI  |
+==============================+==================================+
| Copyright 2024 Zhu jingrui, el al                               |
|                                                                 |
| Licensed under the Apache License, Version 2.0 (the "License"); |
| you may not use this file except in compliance with the License.|
| You may obtain a copy of the License at                         |
|                                                                 |
|    http://www.apache.org/licenses/LICENSE-2.0                   |
|                                                                 |
| Unless required by applicable law or agreed to in writing,      |
| software distributed under the License is distributed on an     |
| "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,    |
| either express or implied.                                      |
| See the License for the specific language governing permissions |
| and limitations under the License.                              |
+-----------------------------------------------------------------+
"""
            )
            exit(0)
    elif command[0] == "help":
        print(helps)
    else:
        if debug:
            try:
                exec(" ".join(command))
            except Exception as e:
                Error(e)
            continue
        if nowProject != "":
            if command[0] == "import":
                fileCommand = oriInput.split("\"")
                if len(fileCommand == 3):
                    files = fileCommand[2].split(" ")
                    seqName = fileCommand[1]

                    name = getName(seqName)
                    seqs = [...]
                    DefaultParser = getattr(aitd.xerlist.ParserList, "aitd-fasta")
                    
                    if len(files) == 2:
                        Par = files[1]
                        DefaultParser = getattr(aitd.xerlist.ParserList, Par)
                        
                    aitd.readFile(files[0], DefaultParser, seqs)
                    
                    for seq in seqs:
                        if os.path.exists(os.path.join(programdict, "data", "sequence", name + ".seq")):
                            with open(programdict + name + ".seq", 'w') as f:
                                f.write(seq.sequence)
                        else:
                            with open(programdict + name + ".seq", 'x') as f:
                                f.write(seq.sequence)
                                
                        if os.path.exists(os.path.join(programdict, "data", "sequence", name + ".metadata")):
                            with open(programdict + name + ".metadata", 'w') as f:
                                f.write(seq.metadata)
                        else:
                            with open(programdict + name + ".seq", 'x') as f:
                                f.write(seq.sequence)
                else:
                    Error(getWord("synerr"))
                    Note("%s : import <name> <file> [<parser>]" % getWord("usage"))
            elif command[0] == "species":
                fullCommand = oriInput.split("\"")
                if len(fullCommand) == 2:
                    speciesName = getName(fullCommand[1])
                    SpeciesList.extend(speciesName)
                else:
                    Error(getWord("synerr"))
                    Note("%s : species <name>" % getWord("usage"))
            elif command[0] == "add":
                if len(command) == 3:
                    if command[1] in SeqMap.keys():
                        SeqMap[command[1]].extend(command[2])
                    else:
                        SeqMap[command[1]] = [...]
                        SeqMap[command[1]].extend(command[2])
                else:
                    Error(getWord("synerr"))
                    Note("%s : add <species> <name>" % getWord("usage"))
            elif command[0] == "del":
                if len(command) == 2:
                    while True:
                        c = input(getWord("confirmSpeciesDel"))
                        if c == 'y':
                            del SeqMap[command[1]]
                            break
                        if c == 'n':
                            break
                if len(command) == 3:
                    while True:
                        c = input(getWord("confirmSeqDel"))
                        if c == 'y':
                            del SeqMap[command[1]][c]
                            break
                        if c == 'n':
                            break
            elif command[0] == "parameter":
                if command[1] == "get" and len(command) == 4:
                    with open(programdict + "setting.json") as js:
                        output = ""
                        dicts = json.load(js.read())
                        if command[2].split("::")[0] == "seq":
                            output = dicts["sequence_list"][command[2]][command[3]]
                        elif command[2].split("::")[0] == "ali":
                            output = dicts["alignment_list"][command[2]][command[3]]
                        elif command[2].split("::")[0] == "tree":
                            output = dicts["tree_list"][command[2]][command[3]]
                        elif command[2].split("::")[0] == "sktch":
                            output = dicts["sketch_list"][command[2]][command[3]]
                        print(output)
                elif command[1] == "set" and len(command) == 5:
                    with open(programdict + "setting.json") as js:
                        dicts = json.load(js.read())
                        if command[2].split("::")[0] == "seq":
                            dicts["sequence_list"][command[2]][command[3]] = command[4]
                        elif command[2].split("::")[0] == "ali":
                            dicts["alignment_list"][command[2]][command[3]] = command[4]
                        elif command[2].split("::")[0] == "tree":
                            dicts["tree_list"][command[2]][command[3]] = command[4]
                        elif command[2].split("::")[0] == "sktch":
                            dicts["sketch_list"][command[2]][command[3]] = command[4]
                            
                        json.dump(dicts, js)
                else:
                    Error(getWord("synerr"))
                    Note("%s : parameter set <object> <key> <value>" % getWord("usage"))
                    Note("%s : parameter get <object> <key>" % getWord("usage"))
            elif command[0] == "align":
                if command[1] == "seq":
                    defaultComparator = "ComparatorList::needleman-wunsch"
                    defaultMatrix = "God know what it is"
                    
                    if len(command) > 4:
                        for i in range(4, len(command) + 1):
                            if command[i].split("=")[0] == "comparator":
                                # comparator
                                cmp = command[i].split("=")[1]
                                defaultComparator = cmp
                            elif command[i].split("=")[0] == "matrix":
                                # matrix
                                mat = command[5].split("=")[1]
                                namespace = getNamespace(cmp.split("::")[0])
                                defaultMatrix = getattr(namespace, mat)
                    
                    print("align seq1 and seq2 with cmp and mat")
                    
                    with open(os.path.join(programdict, "setting.json"), "r") as js:
                        strSeq1 = command[2].split("::")[1]
                        strSeq2 = command[3].split("::")[1]
                        data = json.load(js.read())
                        file1 = data["sequence_list"][command[2]]["file"]
                        file2 = data["sequence_list"][command[3]]["file"]
                        seq1 = seq2 = ""
                        with open(file1, "r") as f:
                            seq1 = f.read()
                        with open(file2, "r") as f:
                            seq2 = f.read()
                        score, alignment, distant = getattr(getNamespace(defaultComparator.split("::")[0]), defaultComparator)(seq1, seq2, defaultMatrix)
                        if os.path.exists(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali")):
                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali"), 'w') as ali:
                                ali.write(alignment[0] + "\n")
                                ali.write(alignment[1])
                        else:
                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali"), 'x') as ali:
                                ali.write(alignment[0] + "\n")
                                ali.write(alignment[1])
                                
                        if os.path.exists(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat")):
                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat"), 'w') as ali:
                                ali.write(score + "\n" + distant)
                        else:
                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat"), 'x') as ali:
                                ali.write(score + "\n" + distant)
                        data["alignment_list"][command[2] + "." + command[3]] = {
                            "file": repr(os.path.join("data","alignment",strSeq1 + "." + strSeq2 + ".ali")),
                            "opposing": [
                                command[2],command[3]
                                ],
                            "data": repr(os.path.join("data", "alignment", strSeq1 + "." + strSeq2 + ".ali.dat")),
                            "algorithm": defaultComparator
                        }


                elif command[1] == "species":
                    pass
                    # To be continued...
                    
            elif command[0] == "tree":
                try:
                    n = int(command[1])
                    
                    if len(command) > n + 1:
                        defaultPlanter = getattr(aitd.xerlist.TreePlanterList, "TreePlanterList::UPGMA")
                        defaultComparator = getattr(aitd.xerlist.ComparatorList, "ComparatorList::needleman-wunsch")
                        defaultMatrix = "God it"
                        isSave = True
                        if len(command) > n + 2:
                            for i in range(n + 2, len(command) + 1):
                                if command[i].split("=")[0] == "planter":
                                    planter = command[i].split("=")[1]
                                    namespace = planter.split("::")[0]
                                    defaultPlanter = getattr(getNamespace(namespace), planter)
                                elif command[i].split("=")[0] == "comparator":
                                    cmp = command[i].split("=")[1]
                                    namespace = getNamespace(cmp.split("::")[0])
                                    defaultComparator = getattr(namespace, cmp)
                                elif command[i].split("=")[0] == "matrix":
                                    mat = command[5].split("=")[1]
                                    namespace = getNamespace(cmp.split("::")[0])
                                    defaultMatrix = getattr(namespace, mat)
                                elif command[i].split("=")[0] == "savealign":
                                    isSave = (command[i].split("=")[1].lower() == "true")
                                    
                        sequenceList = [aitd.Sequence("", "", "")]
                        disMatrix = [[...],...]
                        name = ""
                        with open(os.path.join(programdict, "setting.json")) as js:
                            data = json.load(js.read())
                            for i in range(2, n + 2):
                                seqFile = data["sequence_list"][command[i]]["file"]
                                name += command[i] + "."
                                with open(seqFile,'r') as file:
                                    sequenceList.append(aitd.Sequence("gene", command[i], file.read()))
                                for j in range(i, n + 2):
                                    file1 = data["sequence_list"][command[i]]["file"]
                                    file2 = data["sequence_list"][command[j]]["file"]
                                    seq1 = seq2 = ""
                                    
                                    with open(file1, 'r') as file:
                                        seq1 = file.read()
                                    with open(file2, 'r') as file:
                                        seq2 = file.read()
                                        
                                    score, alignment, distant = defaultComparator(seq1, seq2, defaultMatrix)
                                    disMatrix[i - 1][j - 1] = distant
                                    if isSave:
                                        if os.path.exists(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali")):
                                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali"), 'w') as ali:
                                                ali.write(alignment[0] + "\n")
                                                ali.write(alignment[1])
                                        else:
                                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali"), 'x') as ali:
                                                ali.write(alignment[0] + "\n")
                                                ali.write(alignment[1])
                                                
                                        if os.path.exists(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat")):
                                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat"), 'w') as ali:
                                                ali.write(score + "\n" + distant)
                                        else:
                                            with open(os.path.join(programdict, "data", "alignment", command[2] + "." + command[3] + ".ali.dat"), 'x') as ali:
                                                ali.write(score + "\n" + distant)
                                        data["alignment_list"][command[2] + "." + command[3]] = {
                                            "file": repr(os.path.join("data","alignment",strSeq1 + "." + strSeq2 + ".ali")),
                                            "opposing": [
                                                command[2],command[3]
                                                ],
                                            "data": repr(os.path.join("data", "alignment", strSeq1 + "." + strSeq2 + ".ali.dat")),
                                            "algorithm": defaultComparator
                                        }

                            lis1, lis2 = aitd.UPGMA(sequenceList, disMatrix)
                            with open(os.path.join(programdict, "data", "tree", name + "tree"), 'wb') as file:
                                pickle.dump((lis1,lis2), file)
                except:
                    Error(getWord("synerr"))
                    Note("%s : tree <seqNum> <seq1> <seq2> <seq3>... [<parameter>]" % getWord("usage"))
                
            elif command[0] == "correct":
                try:
                    namespace = getNamespace(command[1].split("::")[0])
                    model = getattr(namespace, command[1])
                    n = int(command[3])
                    pass
                except:
                    pass
                
            elif command[0] == "list":
                try:
                    with open(os.path.join(programdict, "setting.json"), 'r') as js:
                        data = json.load(js.read())
                        if command[1] == "sequence":
                            for key, val in data["sequence_list"].items():
                                print(key, end=": ")
                                print(val["name"], end = ", ")
                                print("description: " + val["description"], end = ", ")
                                print("from: ", val["from"])
                        elif command[1] == "alignment":
                            for key, val in data["alignment_list"].items():
                                print(val["opposing"][0] + " and " + val["opposing"][1], end = " : ")
                                print("algorithm: ", val["algorithm"], end=", ")
                                print("file & data", val["file"] + " & ", val["data"])
                        elif command[1] == "comparator":
                            pass
                        elif command[1] == "matrix":
                            pass
                except:
                    Error(getWord("synerr"))
                    Note("%s : list sequence/alignment/comparator/matrix/" % getWord("usage"))
            elif command[0] == "display":
                try:
                    tree = comma nd[1]
                    disMet = command[2]
                    filetype = command[3]
                except:
                    Error(getWord("synerr"))
                    Note("%s : display <tree> <display> <filetype>" % getWord("usage"))
            ################################################################
            # HERE!!!!!!!!                                                 #
            ################################################################
            continue
        Error(getWord("invcmd"))
        continue

