import os, sys
from . import error
from . import xerlist


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


def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap=-1):
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


if __name__ == "__main__":
    pass
