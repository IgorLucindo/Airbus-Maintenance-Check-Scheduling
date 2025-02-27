import gurobipy as gp
from gurobipy import GRB
from itertools import product
from utils.check_schedulability_utils import *


# run model for schedulling airbusses and return output
def run_model(instance):
    A, C, S, T = instance

    # create model
    model = gp.Model("airbus schedulling")

    # suppress output
    model.setParam("OutputFlag", 0)

    # add variables
    x = model.addVars(A, C, S, T, vtype=GRB.BINARY, name="x")

    # set objective function
    obj_fn = gp.quicksum(x[i, j, s, t] for i, j, s, t in product(A, C, S, T))
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    for i, j, s, t in product(A, C, S, T):
        if not is_schedulable(i, j, s, t):
            x[i, j, s, t].ub = 0
        

    # solve
    model.optimize()

    # return optimal solution
    return [[[[x[i, j, s, t].X for i in A] for j in C] for s in S] for t in T]