import numpy as np
import pandas as pd

def dual_simplex(matrix):
    while np.min(matrix.iloc[1:,0]) <= 0:
        #出基变量
        out_basic = matrix.iloc[1:,0].idxmin()
        #确定进基变量
        in_basic = None
        idxset =  set(list(matrix.loc["rc"].index)[1:]) - set(list(matrix.index)[1:])
        minsita = 1e10
        for idx in idxset:
            if matrix.loc[out_basic,idx] < 0:
                sita = -matrix.loc["rc",idx]/matrix.loc[out_basic,idx]
                if sita < minsita:
                    minsita = sita
                    in_basic = idx
        if in_basic:
            #pivote
            matrix.loc[out_basic,:] = matrix.loc[out_basic,:]/matrix.loc[out_basic,in_basic]
            for idx in matrix.index:
                if idx != out_basic:
                    matrix.loc[idx,:] = matrix.loc[idx,:] - matrix.loc[idx,in_basic]*matrix.loc[out_basic,:]
            matrix.rename(index={out_basic:in_basic},inplace=True)
            #print(matrix)
            #return
        else:
            #infeasible
            print("the LP is infeasible")
            return
    else:
        return -matrix.iloc[0,0]
def simplex(matrix):
    while np.min(matrix.iloc[0,1:]) < 0:
        #进基变量
        in_basic = matrix.iloc[0,1:].idxmin()
        #确定进基变量
        out_basic = None
        idxset =  set(list(matrix.index)[1:])
        minsita = 1e10
        for idx in idxset:
            if matrix.loc[idx,in_basic] > 0:
                sita = matrix.loc[idx,"b"]/matrix.loc[idx,in_basic]
                if sita < minsita:
                    minsita = sita
                    out_basic = idx
        if out_basic:
            #pivote
            matrix.loc[out_basic,:] = matrix.loc[out_basic,:]/matrix.loc[out_basic,in_basic]
            for idx in matrix.index:
                if idx != out_basic:
                    matrix.loc[idx,:] = matrix.loc[idx,:] - matrix.loc[idx,in_basic]*matrix.loc[out_basic,:]
            matrix.rename(index={out_basic:in_basic},inplace=True)
            #print(matrix)
            #return
        else:
            #infeasible
            print("the LP is infeasible")
            return
    else:
        return -matrix.iloc[0,0]
matrix = pd.DataFrame(
    data=np.array([[0,7,2,0,0,0],
                  [4,-1,2,1,0,0],
                   [20,5,1,0,1,0],
                   [-7,-2,-2,0,0,-1]]),
    columns = ["b","x1","x2","x3","x4","x5"],
    index=["rc","x3","x4","x5"]
)
print(matrix)
obj = dual_simplex(matrix.copy())
print(obj)
print(matrix)

matrix = pd.DataFrame(
    data=np.array([[0,-7,-2,0,0,0,1000],
                   [4,-1,2,1,0,0,0],
                   [20,5,1,0,1,0,0],
                   [7,2,2,0,0,-1,1]]),
    columns = ["b","x1","x2","x3","x4","x5","x6"],
    index=["rc","x3","x4","x6"]
)
obj = simplex(matrix.copy())
print(obj)