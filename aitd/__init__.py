import os, sys
from . import error
from . import xerlist
import matplotlib.pyplot as plt
import numpy as np
import copy


def FASTA_parser(data):
    dataList = data.split("\n")
    returnData = []
    for i in dataList:
        if i.startswith(">"):
            returnData.append({"metadata": i.split(">")[1].strip(), "sequence": ""})
            continue
        returnData[-1]["sequence"] += i.strip()
    return returnData


setattr(xerlist.ParserList, "aitd-fasta", FASTA_parser)


def needleman_wunsch(seq1, seq2, match=5, mismatch=-4, gap=-2):
    """
    Needleman-Wunsch 算法实现
    :param seq1: 第一个序列
    :param seq2: 第二个序列
    :param match: 匹配的分数
    :param mismatch: 不匹配的分数
    :param gap: 插入或删除间隙的分数
    :return: 对齐的分数和最佳对齐的矩阵
    """
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    score_matrix = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        score_matrix[i][0] = score_matrix[i - 1][0] + gap
    for j in range(1, cols):
        score_matrix[0][j] = score_matrix[0][j - 1] + gap

    for i in range(1, rows):
        for j in range(1, cols):
            match_score = score_matrix[i - 1][j - 1] + (
                match if seq1[i - 1] == seq2[j - 1] else mismatch
            )
            delete_score = score_matrix[i - 1][j] + gap
            insert_score = score_matrix[i][j - 1] + gap
            score_matrix[i][j] = max(match_score, delete_score, insert_score)

    alignment = []
    i, j = rows - 1, cols - 1
    while i > 0 and j > 0:
        score_current = score_matrix[i][j]
        score_diag = score_matrix[i - 1][j - 1]
        score_up = score_matrix[i - 1][j]
        score_left = score_matrix[i][j - 1]

        if score_current == score_diag + (
            match if seq1[i - 1] == seq2[j - 1] else mismatch
        ):
            alignment.append((seq1[i - 1], seq2[j - 1]))
            i -= 1
            j -= 1
        elif score_current == score_up + gap:
            alignment.append((seq1[i - 1], "-"))
            i -= 1
        else:
            alignment.append(("-", seq2[j - 1]))
            j -= 1

    while i > 0:
        alignment.append((seq1[i - 1], "-"))
        i -= 1
    while j > 0:
        alignment.append(("-", seq2[j - 1]))
        j -= 1

    alignment.reverse()

    return score_matrix[-1][-1], alignment


setattr(xerlist.ComparatorList, "needleman-wunsch", needleman_wunsch)


def process_NW(seq1, seq2):
    alignment = getattr(xerlist.ComparatorList, "needleman-wunsch")(seq1, seq2)[1]
    ans = len(alignment)

    for i in alignment:
        if i[0] == i[1]:
            ans -= 1
    return ans


setattr(xerlist.ProcessorList, "needleman-wunsch", process_NW)

if __name__ == "__main__":
    seq1 = "GATTACA"
    seq2 = "GCATGCU"
    score, alignment = needleman_wunsch(seq1, seq2)
    print("Score:", score)
    print(
        "Alignment:",
        "".join(a[0] for a in alignment),
        "|",
        "".join(a[1] for a in alignment),
    )


def readFile(filename, parser, sequenceList):
    try:
        with open(filename, "r") as file:
            data = parser(file.read())
            for i in range(len(data)):
                try:
                    sequenceList[i].sequence = data[i]["sequence"]
                    sequenceList[i].metadata = data[i]["metadata"]
                except IndexError:
                    raise error.DataMismatchError(
                        f"Too much data in the file '{filename}'."
                    )
    except FileNotFoundError:
        raise error.FileError(f"File '{filename}' not found.")
    except Exception as e:
        raise error.FileError(f"An error occurred while reading file '{filename}': {e}")


class Sequence(object):
    def __init__(self, type, name, sequence=""):
        self.type = type
        self.name = name
        self.sequence = sequence
        self.metadata = None


def compare(a, b, comparator):
    return comparator(a.sequence, b.sequence)[0]


def getMatrixMin(matrix):
    m, n = np.shape(matrix)
    matrixMin = matrix[0][0]
    y = 0
    x = 1
    for i in range(m):
        for j in range(i, n):
            if matrix[j][i] < matrixMin:
                matrixMin = matrix[j][i]
                x = j + 1
                y = i
    return x, y, matrixMin


def createNdm(dic, odm, auxiliaryList, treeMark):
    if len(odm) == 0:
        return auxiliaryList, treeMark
    x, y, matrixMin = getMatrixMin(odm)

    dic1 = copy.deepcopy(dic)
    dic1.pop(list(dic.keys())[list(dic.values()).index(x)])
    dic1.pop(list(dic.keys())[list(dic.values()).index(y)])
    dic1len = len(dic1)
    ndm = np.zeros((dic1len, dic1len))
    index = 0
    for s in dic1.keys():
        if x < dic1[s]:
            d1 = odm[dic1[s] - 1][x]
        else:
            d1 = odm[x - 1][dic1[s]]
        if y < dic1[s]:
            d2 = odm[dic1[s] - 1][y]
        else:
            d2 = odm[y - 1][dic1[s]]
        ndm[dic1len - 1][index] = (d1 + d2) / 2
        dic1[s] = index
        index += 1
    for i in range(dic1len):
        for j in range(i + 1, dic1len):
            ndm[j - 1][i] = odm[
                dic[list(dic1.keys())[list(dic1.values()).index(j)]] - 1
            ][dic[list(dic1.keys())[list(dic1.values()).index(i)]]]
    newSquence = (
        list(dic.keys())[list(dic.values()).index(y)]
        + list(dic.keys())[list(dic.values()).index(x)]
    )
    dic1[newSquence] = index
    list1 = [newSquence, auxiliaryList[y], auxiliaryList[x]]
    list2 = [matrixMin / 2, treeMark[y], treeMark[x]]

    del auxiliaryList[x]
    del auxiliaryList[y]
    del treeMark[x]
    del treeMark[y]
    auxiliaryList.append(list1)
    treeMark.append(list2)
    return createNdm(dic1, ndm, auxiliaryList, treeMark)


def UPGMA(seqs, comparator):
    """
    :seqs: a list of sequences (aitd.Sequence)
    """
    n = len(seqs)
    treeMark = []
    auxiliaryList = []
    dic = {}
    for i in range(n):
        dic[chr(65 + i)] = i
        auxiliaryList.append([chr(65 + i)])
        treeMark.append([chr(65 + i)])
    sequenceList = []
    for i in range(n):
        sequenceList.append(seqs[i].sequence)
    l = len(sequenceList)
    odm = np.zeros((l - 1, l - 1))
    for i in range(l - 1):
        for j in range(i + 1, l):
            odm[j - 1][i] = comparator(sequenceList[i], sequenceList[j])
    getMatrixMin(odm)
    createNdm(dic, odm, auxiliaryList, treeMark)
    return auxiliaryList[0], treeMark[0]
    # drawArrow(auxiliaryList[0], treeMark[0], n + 1, 0, 0, 0)
    # plt.show()


setattr(xerlist.TreePlanterList, "UPGMA", UPGMA)


def drawArrow(auxiliaryList, treeMark, n, m=0, upperX=0, upperY=0,display=True, issave=False, savepath=""):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Phylogenetic tree")
    plt.ylabel("Distance")
    ax.set_xticks([])
    def _drawArrow(auxiliaryList, treeMark, n, m=0, upperX=0, upperY=0,display=True):
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.set_title("Phylogenetic tree")
        # plt.ylabel("Distance")
        # ax.set_xticks([])
        if isinstance(treeMark[0], float):
            x = (m + n) / 2
            if upperX != 0:
                ax.plot((x, upperX), (treeMark[0], upperY), color="k")
            else:
                ax.set_xlim(0, n)
                ax.set_ylim(0, treeMark[0] + 1)
            ax.scatter(x, treeMark[0], c="k", marker="o")
            ax.text(x + 0.05, treeMark[0] + 0.05, treeMark[0])
            ax.scatter((x + n) / 2, treeMark[0], c="k", marker="o", alpha=0)
            ax.scatter((x + m) / 2, treeMark[0], c="k", marker="o", alpha=0)
            ax.plot(((x + n) / 2, x), (treeMark[0], treeMark[0]), color="k")
            ax.plot(((x + m) / 2, x), (treeMark[0], treeMark[0]), color="k")
            _drawArrow(auxiliaryList[2], treeMark[2], n, x, (x + n) / 2, treeMark[0])
            _drawArrow(auxiliaryList[1], treeMark[1], x, m, (x + m) / 2, treeMark[0])
        else:
            x = (m + n) / 2
            ax.plot((x, upperX), (0.05, upperY), color="k")
            ax.scatter(x, 0.02, c="k")
            ax.text(x + 0.05, 0.05, treeMark[0])
    _drawArrow(auxiliaryList, treeMark, n, m, upperX, upperY,display)
    if display:
        plt.show()
    if issave:
        plt.savefig(savepath)


setattr(xerlist.DisplayList, "custom", drawArrow)

# if __name__ == "__main__":
#     from aitd import *

#     seqs = [
#         Sequence("DNA", "Seq1", "GATTACA"),
#         Sequence("DNA", "Seq2", "GCATGCU"),
#         Sequence("DNA", "Seq3", "GACTACG"),
#         Sequence("DNA", "Seq4", "CTGAGCT"),
#     ]
#     tree = getattr(xerlist.TreePlanterList, "UPGMA")(
#         seqs, getattr(xerlist.ProcessorList, "needleman-wunsch")
#     )

#     # print(tree[0],tree[1])

#     getattr(xerlist.DisplayList, "custom")(tree[0],tree[1],4+1)

if __name__ == "__main__":
    pass