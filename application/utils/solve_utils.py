import gurobipy as gp
from gurobipy import GRB
from itertools import product
from utils.check_schedulability_utils import *


# model for solving schedulling airbusses and return output
def solve_aircraft_scheduling(instance):
    A, C, S, S_ijt, T, sta_specs, airbus_check, check_days, check_daytogo = instance

    # create model
    model = gp.Model("airbus schedulling")

    # suppress output
    model.setParam("OutputFlag", 1)

    # add variables
    x = model.addVars(A, C, S, T, vtype=GRB.BINARY, name="x")
    y = model.addVars(A, S, T, vtype=GRB.BINARY, name="y")

    # set objective function
    obj_fn = gp.quicksum(x[i, j, s, t] for i, j, s, t in product(A, C, S, T))
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    # constraint - fix the value of non schedulable i, j, s, t to 0
    for i, j, s, t in product(A, C, S, T):
        if not is_schedulable(i, j, t, S_ijt, airbus_check):
            x[i, j, s, t].ub = 0

    # constraint - airbus cannot be scheduled in more than 1 station
    model.addConstrs((gp.quicksum(x[i, j, s, t] for s in S) <= 1 for i, j, t in product(A, C, T)), name="c1")
    # constraint - airbus cannot be schedule an A-check and Phase-check at the same time
    model.addConstrs((x[i, 'A', s, t] + y[i, s, t] <= 1 for i, s, t in product(A, S, T)), name="c2")
    model.addConstrs((x[i, j, s, t] <= y[i, s, t] for i, j, s, t in product(A, C[1:], S, T)), name="c3")
    # constraint - airbus must be scheduled within its initial maximum allowable interval (days_to_go)
    model.addConstrs(
        (gp.quicksum(gp.quicksum(x[i, j, s, tau] for s in S_ijt[i][j][tau]) for tau in range(check_daytogo[i][j]) if tau in S_ijt[i][j]) >= 1 
         for i in A for j in airbus_check[i]),
        name="c4"
    )
    # constraint - airbus must be scheduled within its maximum allowable interval
    model.addConstrs(
        (gp.quicksum(gp.quicksum(x[i, j, s, tau] for s in S_ijt[i][j][tau]) for tau in range(t, t + check_days[j]) if tau in S_ijt[i][j]) >= 1
         for i, t in product(A, T) for j in airbus_check[i] if t < T[-1] - check_days[j]),
        name="c5"
    )
    # constraint - station has maximum capacity of A-checks
    model.addConstrs((gp.quicksum(x[i, 'A', s, t] for i in A) <= sta_specs[s]['A'] for s, t in product(S, T)), name="c6")
    # constraint - station has maximum capacity of Phase-checks
    model.addConstrs((gp.quicksum(x[i, j, s, t] for i in A) <= sta_specs[s]['P'] for j, s, t in product(C[1:], S, T)), name="c7")
    # constraint - station has maximum capacity of checks
    model.addConstrs((gp.quicksum(x[i, j, s, t] for i in A) <= sta_specs[s]['STATION_CAP'] for j, s, t in product(C, S, T)), name="c8")
    # constraint - airbus cannot be scheduled at the same station again within 3 days
    model.addConstrs((gp.quicksum(x[i, j, s, tau] for tau in range(t, t + 3)) <= 1 for i, j, s, t in product(A, C, S, T) if t < T[-1] - 3), name="c9")

    # solve
    model.optimize()

    # return optimal solution
    return [x[i, j, s, t].X for i, j, s, t in product(A, C, S, T)]