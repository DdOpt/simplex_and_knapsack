import numpy as np
import pandas as pd

#nums of items
n = 4
#weight of items
w = [0,2,3,4,5]
#profit of item
v = [0,50,19,23,28]
#capacity of Knapsack
K = 7
def knapsack(w,v,K):
    table = [[0]*len(w) for i in range((K+1))]
    #动态更新
    for i in range(len(w)):
        for j in range(K+1):
            if j >= w[i]:
                table[j][i] = max(table[j][i-1],table[j-w[i]][i-1]+v[i])
            else:
                table[j][i] = table[j][i-1]
    res = [0] * len(w)
    #回溯
    def trace_back():
        k = K
        j = len(w)-1
        while k and table[k][j]:
            if table[k][j] != table[k][j-1]:
                k -= w[j]
                res[j] = 1
            j -= 1
    trace_back()
    return table,res
def integerKnapsack(w,v,K):
    table = [[0] * len(w) for i in range((K + 1))]
    for i in range(len(w)):
        for j in range(K + 1):
            if j >= w[i]:
                table[j][i] = max(table[j][i-1], table[j-w[i]][i] + v[i]) #更新的是本阶段的table[j-w[i]][i]+ v[i]
            else:
                table[j][i] = table[j][i-1]
    #回溯
    def trace_back(k,j):
        if table[k][j] == table[k][j-1]:
            return 0
        else:
            return 1 + trace_back(k-w[j],j)
    k = K
    j = len(w)-1
    solution = [0] * len(w)
    while j > 0:
        solution[j] = trace_back(k,j)
        j -= 1
        k = K - np.array(solution).dot(np.array(w))
    return table,solution

print("************Binary***********")
table,solution = knapsack(w,v,K)
dt = pd.DataFrame(
    data = np.array(table),
    columns=[i for i in range(len(w))],
    index = [i for i in range(K+1)])
print(dt)
print(solution)


print("***********Integer*************")
table,solution = integerKnapsack(w,v,K)
dt = pd.DataFrame(
    data = np.array(table),
    columns=[i for i in range(len(w))],
    index = [i for i in range(K+1)])
print(dt)
print(solution)