#引入库
import numpy as np
import random as rd
from scipy.optimize import minimize
class model:
    def __init__(self):
        self.c1=np.ones((5,3,3))#本组数据
        self.c2=np.ones((3,1,1))#外组数据
        self.maxt=10#最多遍历次数
        self.mine=1000#最小误差
        self.step=10#步长
    def sumResidual(self):#求当前残差和
        r=0
        for c in self.residual:
            for dc in c:
                r=r+np.exp(dc[1])
        return r
    def addId(self,Id,i):
        if Id < 45:
            self.c1[Id%5][(Id//5)%3][Id//15]+=i
        else:
            self.c2[(Id-45)%3][(Id-45)%1][(Id-45)%1]+=i
    def change(self):#处理变动函数
        i=0
        for c in range(0,len(self.residual)):
            maxyResidual=-1
            maxId=0
            id1=-1
            for dc in range(0,len(self.residual[c])):
                yResidual=0
                for y in self.residual[c][dc]:
                    print (y,dc)
                    yResidual=yResidual+np.exp(y)
                if maxyResidual<=yResidual:
                    maxyResidual=yResidual
                    maxId=id1
                id1=id1+1
            self.addId(i,self.getStep()*maxId)
            i=i+1
                
    def getDistance(self,vector1=np.array([]),vector2=np.array([])):
        return np.sum((vector1-vector2)**2)
    def compute(self,tree=np.array([[[]]]),v=np.array([[]]),l=np.array([[]]),goal=np.array([[]])):
        for i in range(0,len(tree)):
            r=np.array([])
            for j in range(0,48):
                maxId=self.fmax(self.allf,goal[i],args=(tree[i],v[i],l[i]))
                r=np.append(r,maxId)
                for d in range(0,3):
                    self.addId(j,d-1)
                    self.residual[j][d][i]=self.allf(goal[i],tree[i],v[i],l[i])/self.allf(maxId.x,tree[i],v[i],l[i])
                    self.addId(j,1-d)

            print(r)
                    
    def fmax(self,func, x0, args=(), **kwargs):
        return minimize(lambda x,tree,v,l:-func(x,tree,v,l), x0, args=args, jac=self.jac, options={'maxiter':100}, **kwargs)
        
    def jac(self,x=np.array([]),tree=np.array([[]]),v=np.array([]),l=np.array([])):
        d=np.zeros((48))
        print(tree,v,l,12341234)
        treeDistance=np.array([])
        for j in range(0,len(tree)):
            treeDistance=np.append(treeDistance,self.getDistance(tree[j],x))
        for i in range(0,len(treeDistance)):
            d=d+self.df(treeDistance,v,l,i)
    def allf(self,x=np.array([]),tree=np.array([[]]),v=np.array([]),l=np.array([])):
        rt=0
        print(tree,v,l,12432)
        treeDistance=np.array([])
        for j in range(0,len(tree)):
            treeDistance=np.append(treeDistance,self.getDistance(tree[j],x))
        for i in range(0,len(treeDistance)):
            rt+=self.f(treeDistance,v,l,i)
        return rt
    def df(self,r=np.array([[]]),v=np.array([]),l=np.array([]),i=0):
        j=0
        rt=np.zeros((48))
        while j<len(r):
            if r[j]==0:
                r[j]+=0.0001
            if j==i:
                for i1 in range(0,5):
                    for i2 in range(0,3):
                        for i3 in range(0,3):
                            rt[i1*9+i2*3+i3]+=(i1-2)*(r[j]**(i1-3))*(l[j]**(i2-1))*(v[j]**(i3-1))*self.c1[i1][i2][i3]
                            print(rt[i1*9+i2*3+i3],i1,i2,i3,r[j],l[j],v[j],(r[j]**(i1-3)),(l[j]**(i2-1)),(v[j]**(i3-1)),7426)
            else:
                for i1 in range(0,3):
                    for i2 in range(0,1):
                        for i3 in range(0,1):
                            rt[i1*1+i2*1+i3*1+45]+=(i1-1)*(r[j]**(i1-2))*(l[j]**(i2-0))*(v[j]**(i3-0))*self.c2[i1][i2][i3]
            j=j+1
        print(rt,2937)
        return rt
    def f(self,r=np.array([[]]),v=np.array([]),l=np.array([]),i=0):
        j=0
        score=0
        while j<len(r):
            if r[j]==0:
                r[j]+=0.0001
            if j==i:
                for i1 in range(0,5):
                    for i2 in range(0,3):
                        for i3 in range(0,3):
                            score=score+(r[j]**(i1-2))*(l[j]**(i2-1))*(v[j]**(i3-1))*self.c1[i1][i2][i3]
            else:
                for i1 in range(0,3):
                    for i2 in range(0,1):
                        for i3 in range(0,1):
                            score=score+(r[j]**(i1-1))*(l[j]**(i2-0))*(v[j]**(i3-0))*self.c2[i1][i2][i3]
            j=j+1
        return score
    def getStep(self):
        return np.exp(-rd.random()-self.t)*self.step
    def training(self,tree=np.array([[[]]]),v=np.array([[]]),l=np.array([[]]),goal=np.array([[]])):
        #第一层是样本个数，第二层是对应基因树
        self.residual=np.zeros((48,3,len(tree)))#共4层，最外面一层是不同变量，第二层是移动量，第三层是不同样本
        self.t=0
        tree=tree.astype(np.float16)
        v=v.astype(np.float16)
        l=l.astype(np.float16)
        goal=goal.astype(np.float16)
        
        print('begin')
        while self.t<self.maxt or self.mine < self.sumResidual():
            self.compute(tree,v,l,goal)

            self.change()
            self.t+=1
            print(self.t)
    def worked(self,tree=np.array([[]]),v=np.array([]),l=np.array([])):
        return self.fmax(self.allf,np.mean(tree,axis=0),args=(tree,v,l)).x

a=model()
a.training(np.array([[[1,2,3],[1,2,3],[1,2,3]],[[2,3,4],[2,3,4],[2,3,4]]]),np.array([[1,2,3],[2,3,4]]),np.array([[3,2,1,],[4,3,2]]),np.array([[1,2,3],[2,3,4]]))