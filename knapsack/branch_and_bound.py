from gurobipy import *
import copy
import numpy as np
class BB:
    def __init__(self,model,obj,candidated_vars,lowerbound,upbound,solution):
        self.model = model
        self.obj = obj
        self.candidated_vars = candidated_vars.copy()
        self.lowerbound = lowerbound
        self.upbound = upbound
        self.solution = solution
        assert upbound >= lowerbound
    def solve(self):
        self.model.Params.OutputFlag = 0
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            self.obj = self.model.objVal
            self.solution = [v.x for v in self.model.getVars()]
            #print(self.solution)
            self.update_up()
            if self.is_integer():
                self.update_lb()
            else:
                self.lowerbound = 0
            return True
        else:
            return False
    def update_lb(self):
        self.lowerbound = self.obj
    def update_up(self):
        if self.upbound > self.obj:
            self.upbound = self.obj
    def branch(self,flac):
        candidated = self.candidated_vars.copy()
        #print(self.solution,candidated,flac)
        if candidated and flac in candidated:
            candidated.remove(flac)
            self.leftchild, self.rightchild = self.model.copy(), self.model.copy()
            self.leftchild.addConstr(self.leftchild.getVars()[flac] <= 0)
            self.rightchild.addConstr(self.rightchild.getVars()[flac] >= 1)
            return BB(self.leftchild,self.obj,candidated,self.lowerbound,self.upbound,self.solution), \
                   BB(self.rightchild, self.obj,candidated, self.lowerbound, self.upbound, self.solution)
        return None,None
    def getFlac(self):
        idx = []
        flac = 0
        load = 0

        for i,vx in enumerate(self.solution):
            if np.isclose(vx,1.0,atol=1e-6):
                idx.append(i)
                load += weight[i]
            elif np.isclose(vx,0.0,atol=1e-6):
                continue
            else:
                #print(self.solution)
                #print(i,self.solution[i])
                flac = i
                idx.append(i)
                load += weight[i]
        #print("flac",flac)
        return idx,flac,load
    def is_integer(self):
        for num in self.solution:
            if np.isclose(num,np.round(num),atol=1e-6):
                continue
            return False
        return True
    def cover_cut(self):
        idx,flac,load = self.getFlac()
        flag = 1
        if load > capacity:
            for i in idx:
                if (load - weight[i]) <= capacity:
                    continue
                flag = 0
                break
        if flag:
            self.model.addConstr(quicksum(self.model.getVars()[i] for i in idx) <= len(idx)-1)
            return True,flac
        else:
            return False,flac
    def candidatedvars_isempty(self):
        if self.candidated_vars:
            return False
        return True

global weight,profit,capacity
n = 7
#weight of items
#weight= [2,3,4,5]
weight= [40,50,30,10,10,40,30]
#profit of item
#profit= [16,19,23,28]
profit= [40,60,10,10,3,20,60]
#capacity of Knapsack
capacity = 100
#capacity = 7
m = Model()
x = m.addVars(n,lb=0,ub=1,vtype=GRB.CONTINUOUS)
m.setObjective(quicksum(profit[i]*x[i] for i in range(n)),sense = GRB.MAXIMIZE)
m.addConstr(quicksum(weight[i]*x[i] for i in range(n)) <= capacity)
m.Params.OutputFlag = 0
m.optimize()
solution = [v.x for v in m.getVars()]
obj = m.objVal
candidated_vars = [i for i in range(n)]
upbound = obj
lowerbound = 0
root = BB(m,obj,candidated_vars,lowerbound,upbound,solution)
queue = [root]
flag,flac = queue[0].cover_cut()
integer = 0
while queue:
    #print(len(queue))
    node = queue.pop(0)
    #print(node)
    #print(flag,flac)
    if flag:
        print("cut", node.solution, node.obj)
        node.solve()
        node.model.update()
        if node.lowerbound > lowerbound:
            lowerbound = node.lowerbound
            sol = node.solution.copy()
            integer = 1
            print("integer solution")
            continue
        queue.append(node)
        node = queue.pop(0)
        #continue
    node.solve()
    if integer and node.obj <= lowerbound:
        continue
    flag, flac = node.cover_cut()
    print("no cut",node.solution,node.obj)
    if node.lowerbound > lowerbound:
        lowerbound = node.lowerbound
        sol = node.solution.copy()
        integer = 1
        print("integer solution")
        continue
    if not node.candidatedvars_isempty():
        lc,rc = node.branch(flac)
        #print(lc)
        if lc:
            queue.append(lc)
            queue.append(rc)

print(sol)
print(lowerbound)