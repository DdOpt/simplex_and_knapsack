from gurobipy import *
import numpy as np

#w = [1,2,2,3,4]
capacity = 60
w = [np.random.randint(1,capacity-30) for i in range(capacity-50)]
A = np.eye(len(w))
b = np.ones(len(w))
try:
    #the rmp model
    masterpro = Model("rmp")
    y = masterpro.addMVar(len(w),obj=1,vtype=GRB.CONTINUOUS,name="p")
    set_partition = masterpro.addMConstr(A,y,"=",b)
    masterpro.Params.OutputFlag = 0
    masterpro.optimize()
    #get the duals
    dual = masterpro.getAttr(GRB.Attr.Pi,masterpro.getConstrs())

    #the price probelm model
    pricepro = Model("pricepro")
    x = pricepro.addVars(len(w),vtype=GRB.BINARY,name="x")
    pricepro.addConstr(quicksum(x[i]*w[i] for i in range(len(w)))<=capacity)
    #the primal price problem objective function is to minimize (c-sum(dual[i]*x[i] for i in range(len(w))),where c = 1
    #when the obj is less than 0,it means that there is a new varible can be added to the RMP.
    #in fact,I have changed this obj to maximize sum(dual[i]*x[i] for i in range(len(w))
    #when the obj is lager than 1,it means that there is a new varible can be added to the RMP.
    #the last objective function can be easily to change the coffe of variable
    pricepro.setObjective(quicksum(x[i]*dual[i] for i in range(len(w))),sense=GRB.MAXIMIZE)
    pricepro.Params.OutputFlag = 0
    pricepro.optimize()
    p = len(w)-1
    while pricepro.objVal > 1:
        #print(masterpro.objVal," ",pricepro.objVal)
        p += 1
        #get a column for the new variable
        coeff =pricepro.getAttr("X",pricepro.getVars())
        column = Column(coeff,masterpro.getConstrs())
        masterpro.addVar(obj=1.0,vtype=GRB.CONTINUOUS,name="p_"+str(p),column=column)
        masterpro.optimize()
        #change variables' coeff of priceproblem in the objective function
        for i in range(len(w)):
            x[i].obj = set_partition[i].pi
        pricepro.optimize()
    #after CG processe, we need to make the varibles in RMP to be Binary.
    for v in masterpro.getVars():
        v.setAttr("VType",GRB.BINARY)
    masterpro.optimize()
    masterpro.write("master.lp")
    print("the total knapsacks need to use: ",masterpro.objVal)
    solution = masterpro.getAttr("X",masterpro.getVars())
    #print(solution)
    for i in range(len(solution)):
        if solution[i] > 0.5:
            print(f"patten {i} is select")
except GurobiError as e:
    print("Erro code "+str(e.errno)+":"+str(e))
