import os, sys
import aitd
import json
import pickle
import yaml
from colorama import Fore, Back, Style

argv = sys.argv

programdict = os.path.dirname(os.path.abspath(__file__))


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


def Renote(message, end):
    print("       %s" % message, end=end)


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


def getword(word):
    if word in langdata:
        return langdata[word]
    elif word in endata:
        return endata[word]
    else:
        Fatal("Unable to find corresponding language information: %s" % word)
        exit(-1)


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
        Fatal("Unable to load language file: %s.yml" % (config["language"]))
        langdata = endata
        return False
    return True


refresh_setting()


def mkdir(path):
    Renote("%s %s..." % (getword("createdict"), path), end=" ")
    try:
        os.makedirs(path)
        print("done.")
        return True
    except Exception:
        print()
        Error("%s : %s" % (getword("dictnotcreate"), path))
        return False


def mkfile(filename, mode="w"):
    Renote("%s %s..." % (getword("createfile"), filename), end=" ")
    try:
        open(filename, "w").close()
        print(getword("done"))
        return True
    except Exception:
        print()
        Error("%s : %s" % (getword("filenotcreate"), filename))
        return False


print(
    """
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
)

nowproject = ""
debug = False

while True:
    if nowproject == "":
        ouinput = 'AITD "%s"> ' % os.getcwd()
    else:
        ouinput = (
            'AITD "%s" ' % os.getcwd()
            + Fore.MAGENTA
            + 'with the project "%s"' % nowproject
            + Style.RESET_ALL
            + ">"
        )
    if debug:
        ouinput = Fore.CYAN + "[DEBUG] " + Style.RESET_ALL + ouinput
    command = input(ouinput).split()
    if len(command) == 0:
        continue
    elif command[0] == "setting":
        if len(command) < 3:
            Error(getword("synerr"))
            Note("%s : setting <option> <value>" % getword("usage"))
            continue
        if command[1] == "language":
            config["language"] = command[2]
            with open("data/setting.dat", "wb") as f:
                pickle.dump(config, f)
            if refresh_setting():
                Note("%s %s" % (getword("langset"), config["language"]))
        else:
            Error(getword("notsetting"))
    elif command[0] == "new":
        if len(command) < 3:
            Error(getword("synerr"))
            Note("%s : new <type> <name> [<parameter>]" % getword("usage"))
            continue
        if command[1] == "project":
            Note(getword("mkpj"))
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
            Note(getword("pjcreated"))
        else:
            Error(getword("synerr"))
            Note("%s : new <type> <name> [<parameter>]" % getword("usage"))
            continue
    elif command[0] == "open":
        if len(command) == 2:
            try:
                os.chdir(os.path.join(os.getcwd(), command[1]))
                nowproject = command[1]
            except FileNotFoundError:
                Error(getword("notpjdict"))
                nowproject = ""
                continue
        else:
            nowproject = os.path.split(os.getcwd())[1]
        # try:
        #     nowproject = command[1]
        # except IndexError:
        #     Error(getword("synerr"))
        #     Note("%s : open <name>" % getword("usage"))
        #     continue
        try:
            with open(os.path.join("setting.json"), "r") as f:
                if json.load(f) == {}:
                    Warning(getword("warnbasic"))
        except Exception:
            Error(getword("wpj"))
            nowproject = ""
            continue
    elif command[0] == "debug":
        if len(command) == 1 or command[1] == "on":
            debug = True
        elif command[1] == "off":
            debug = False
        else:
            Error(getword("synerr"))
            Note("%s : debug [on|off]" % getword("usage"))
            continue
    elif command[0] == "exit":
        Note(getword("exit"))
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
    else:
        if debug:
            try:
                exec(" ".join(command))
            except Exception as e:
                Error(e)
            continue
        if nowproject != "":
            if command[0] == "exit":
                Note(getword("exitpj"))
                os.chdir(os.path.join(os.getcwd(), ".."))
                nowproject = ""
            ################################################################
            # HERE!!!!!!!!                                                 #
            ################################################################
            continue
        Error(getword("invcmd"))
        continue
