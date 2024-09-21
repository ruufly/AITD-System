import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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



def alignment(A, B):
    seq1 = open(f"{A}.seq","r").read()
    seq2 = open(f"{B}.seq","r").read()
    score, alignment = needleman_wunsch(seq1, seq2)
    ans = len(alignment)
    for i in alignment:
        if i[0] == i[1]:
            ans -= 1
    with open(f"..\\alignment\\{A}.{B}.ali","w") as f:
        f.write("".join(a[0] for a in alignment))
        f.write("\n")
        f.write("".join(a[1] for a in alignment))
    with open(f"..\\alignment\\{A}.{B}.ali.dat","w") as f:
        f.write(f"{score}\n{ans}")

alignment("EColiccmC", "EColiccmE")