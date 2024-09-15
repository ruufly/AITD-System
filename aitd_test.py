from aitd import *

seq1 = Sequence("DNA", "A")
seq2 = Sequence("DNA", "B")

readFile("aitd_test.dat", FASTA_parser, [seq1, seq2])

print(compare(seq1, seq2, needleman_wunsch))

print(needleman_wunsch("GATTACA","GCATGCU"))

"""
G-ATTACA
GCA-TGCU

G-AT-TAC-A
GCATG--CU-
"""