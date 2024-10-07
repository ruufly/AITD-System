# 引入库
# import cupy as cp
import numpy as cp
import random as rd
from scipy.optimize import minimize
import pickle
import json

N = 5
M = 3
L = 3
K = 1


class model:
    def __init__(self):

        self.c1 = cp.ones((N, M))  # 本组数据
        self.c2 = cp.ones((L, K))  # 外组数据
        self.maxt = 2  # 最多遍历次数
        self.mine = 1000  # 最小误差
        self.step = 10  # 步长
        self.mint = 1  # 最少遍历次数
        self.istraining = 0

    def save(self, files):
        f = open(files, "wb")
        s = [self.c1, self.c2]
        pickle.dump(s, f)
        f.close()

    def read(self, files):
        f = open(files, "rb")
        s = pickle.load(f)
        self.c1 = s[0]
        self.c2 = s[1]
        f.close()

    def b(self, a=cp.array([])):  # 标准化
        #    print(a)
        mx = a.max()
        for i in range(0, len(a)):
            a[i] /= mx
        return a

    #  print(a,1)
    def sumResidual(self):  # 求当前残差和
        r = 1
        for c in self.residual:
            for dc in c:
                r += cp.exp(-dc[0])
        return r

    def addId(self, Id, i):
        if Id < N * M:
            self.c1[Id % N][(Id // N) % M] += i
        else:
            self.c2[(Id - N * M) % L][(Id - N * M) % K] += i

    def change(self):  # 处理变动函数
        i = 0
        for c in range(0, len(self.residual)):
            maxyResidual = -1
            maxId = 0
            id1 = -1
            for dc in range(0, len(self.residual[c])):
                yResidual = 0
                for y in self.residual[c][dc]:
                    #        print (y,dc)
                    yResidual = yResidual + cp.exp(y)
                if maxyResidual <= yResidual:
                    maxyResidual = yResidual
                    maxId = id1
                id1 = id1 + 1
            self.addId(i, self.getStep() * maxId)
            i = i + 1

    def getDistance(self, vector1=cp.array([]), vector2=cp.array([])):
        #  print((vector1-vector2),427)
        return cp.sum((vector1 - vector2) ** 2)

    def compute(self, tree=cp.array([[[]]]), l=cp.array([[]]), goal=cp.array([[]])):
        for i in range(0, len(tree)):
            r = cp.array([])
            for j in range(0, 48):
                maxId = self.fmax(self.allf, goal[i], args=(tree[i], l[i]))
                r = cp.append(r, maxId)
                for d in range(0, 3):
                    self.addId(j, d - 1)
                    #              print(maxId.x,5244)
                    self.residual[j][d][i] = self.allf(
                        goal[i], tree[i], l[i]
                    ) / self.allf(maxId.x, tree[i], l[i])
                    self.addId(j, 1 - d)

        #   print(r)

    def fmax(self, func, x0, args=(), **kwargs):
        return minimize(
            lambda x, tree, l: -func(x, tree, l),
            x0,
            args=args,
            # options={"maxiter": 100},
            **kwargs
        )

    def jac(self, x=cp.array([]), tree=cp.array([[]]), l=cp.array([])):
        d = cp.zeros((48))
        #    print(tree,l,12341234)
        treeDistance = cp.array([])
        for j in range(0, len(tree)):
            treeDistance = cp.append(treeDistance, self.getDistance(tree[j], x))
        for i in range(0, len(treeDistance)):
            d = d + self.df(treeDistance, l, i)

    def allf(self, x=cp.array([]), tree=cp.array([[]]), l=cp.array([])):
        rt = 0
        #   print(tree,l,12432)
        treeDistance = cp.array([])
        for j in range(0, len(tree)):
            treeDistance = cp.append(treeDistance, self.getDistance(tree[j], x))
        #   print(treeDistance[j])
        #  print(treeDistance,234)
        #  if not self.istraining:
        #   print(treeDistance)
        for i in range(0, len(treeDistance)):
            rt += self.f(treeDistance, l, i)
        return rt

    def df(self, r=cp.array([[]]), l=cp.array([]), i=0):
        j = 0
        rt = cp.zeros((48))
        while j < len(r):
            if r[j] == 0:
                r[j] += 0.0001
            if j == i:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        rt[i1 * 9 + i2 * 3] += (
                            (i1 - 2)
                            * (r[j] ** (i1 - 3))
                            * (l[j] ** (i2 - 1))
                            * self.c1[i1][i2]
                        )
            #                     # print(rt[i1*9+i2*3+i3],i1,i2,i3,r[j],l[j](r[j]**(i1-3)),(l[j]**(i2-1)),(v[j]**(i3-1)),7426)
            else:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        rt[i1 * 1 + i2 * 1 + N * M] += (
                            (i1 - 1)
                            * (r[j] ** (i1 - 2))
                            * (l[j] ** (i2 - 0))
                            * self.c2[i1][i2]
                        )
            j = j + 1
        # print(rt,2937)
        return rt

    def f(self, r=cp.array([]), l=cp.array([]), i=0):
        j = 0
        score = 0
        #     if not self.istraining:
        #         print(l)
        #     print(r,l)
        while j < len(r):
            if r[j] == 0:
                r[j] += 0.0001
            if j == i:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        #     if not self.istraining:
                        #          print(r[j],i1,l[j],i2,self.c1[i1][i2],816)
                        score = (
                            score
                            + (r[j] ** (i1 - 2)) * (l[j] ** (i2 - 1)) * self.c1[i1][i2]
                        )
            else:
                for i1 in range(0, L):
                    for i2 in range(0, K):
                        #        print(r[j],i1,l[j],i2)
                        score = (
                            score
                            + (r[j] ** (i1 - 1)) * (l[j] ** (i2 - 0)) * self.c2[i1][i2]
                        )
            j = j + 1
        return score

    def getStep(self):
        return cp.exp(-rd.random() - self.t) * self.step

    def training(self, tree=cp.array([[[]]]), l=cp.array([[]]), goal=cp.array([[]])):
        # 第一层是样本个数，第二层是对应基因树
        self.istraining = 1
        self.residual = cp.zeros(
            (48, 3, len(tree))
        )  # 共4层，最外面一层是不同变量，第二层是移动量，第三层是不同样本
        self.t = 0
        tree = tree.astype(cp.float16)
        for i in tree:
            for j in tree:
                self.b(j)
        l = l.astype(cp.float16)
        for i in l:
            self.b(i)
        goal = goal.astype(cp.float16)
        for i in goal:
            self.b(i)

        print("begin")
        while (
            (self.t < self.maxt) and (self.mine < self.sumResidual())
        ) or self.t < self.mint:
            self.compute(tree, l, goal)
            print(self.t)
            self.change()
            self.t += 1
        self.istraining = 0

    def worked(self, tree=cp.array([[]]), l=cp.array([])):

        tree = tree.astype(cp.float16)
        mx = tree.max()
        for i in tree:
            self.b(i)
        l = l.astype(cp.float16)
        self.b(l)
        return self.fmax(self.allf, cp.mean(tree, axis=0), args=(tree, l)).x * mx


def sdf(a=cp.array([[]])):
    s = cp.array([])
    for i in a:
        for j in i:
            s = cp.append(s, j)
    return s


# ek = []
# eue = []
# euc = []
# for i in range(1,4):
# # i = 1
#     k = []
#     for j in range(5):
#         print("READIN: %d %d" % (i,j))
#         with open("output_%d\\output_%d%d_.json" % (i,i,j),"r") as f:
#             data = json.load(f)
#             # print(sdf(cp.array(data)).tolist())
#             k.append(sdf(cp.array(data)).tolist())
#     # print(k)
#     # k = cp.array(k)
#     with open("output_%d\\output_%dA_.json" % (i,i),"r") as f:
#         ue = json.load(f)
#     ue = sdf(cp.array(ue)).tolist()
#     uc = [100 for i in range(100)]
#     ek.append(k)
#     eue.append(ue)
#     euc.append(uc)


# a = model()
# a.training(
#     cp.array(ek),
#     cp.array(euc),
#     cp.array(eue),
# )
# a.save("modelA.model")


def runmodel(modelpath, distances, lengths):
    a = model()
    a.read(modelpath)
    return a.worked(cp.array(distances), cp.array(lengths)).tolist()
