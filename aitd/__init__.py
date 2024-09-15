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


def Needleman_Wunsch(seq1, seq2):
    # Define the scoring matrix
    match = 2
    mismatch = -1
    gap_penalty = -1
    # Initialize the matrix
    m = len(seq1) + 1
    n = len(seq2) + 1
    matrix = [[0] * n for _ in range(m)]
    # Fill in the matrix
    for i in range(1, m):
        matrix[i][0] = matrix[i - 1][0] + gap_penalty
    for j in range(1, n):
        matrix[0][j] = matrix[0][j - 1] + gap_penalty
    for i in range(1, m):
        for j in range(1, n):
            if seq1[i - 1] == seq2[j - 1]:
                score = match
            else:
                score = mismatch
            matrix[i][j] = max(
                matrix[i - 1][j] + gap_penalty,
                matrix[i][j - 1] + gap_penalty,
                matrix[i - j] + score,
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


if __name__ == "__main__":
    pass
