import gurobipy as gp
from gurobipy import GRB
from itertools import product
from utils.check_schedulability_utils import *


# model for solving schedulling airbusses and return output
def solve_aircraft_scheduling(instance):
    A, C, S, T, sta_specs = instance

    # create model
    model = gp.Model("airbus schedulling")

    # suppress output
    model.setParam("OutputFlag", 0)

    # add variables
    x = model.addVars(A, C, S, T, vtype=GRB.BINARY, name="x")
    y = model.addVars(A, S, T, vtype=GRB.BINARY, name="y")

    # set objective function
    obj_fn = gp.quicksum(x[i, j, s, t] for i, j, s, t in product(A, C, S, T))
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    for i, j, s, t in product(A, C, S, T):
        if not is_schedulable(i, j, s, t, sta_specs):
            x[i, j, s, t].ub = 0

    model.addConstrs((gp.quicksum(x[i, j, s, t] for s in S) <= 1 for i, j, t in product(A, C, T)), name="c1")

    model.addConstrs((x[i, 'AC', s, t] + y[i, s, t] <= 1 for i, s, t in product(A, S, T)), name="c2")
    model.addConstrs((x[i, j, s, t] <= y[i, s, t] for i, j, s, t in product(A, CC, S, T)), name="c3")
        

    # solve
    model.optimize()

    # return optimal solution
    return [x[i, j, s, t].X for i, j, s, t in product(A, C, S, T)]