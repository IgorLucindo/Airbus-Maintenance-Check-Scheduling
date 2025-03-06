# check if x_ijst is schedulable
def is_schedulable(i, j, t, S_ijt, airbus_check):
    return i in S_ijt and j in S_ijt[i] and t in S_ijt[i][j] and is_check_airbus(j, i, airbus_check)


# check if station s is compatible with airbus i
def is_station_airbus_date(i, s, t, airbus_subfleet, station_airbus_date):
    return t in station_airbus_date[s] and airbus_subfleet[i] in station_airbus_date[s][t]


# check if station s has capability for check j (set S_j)
def is_station_check(s, j, sta_specs):
    j_str = 'P'
    if j == 0:
        j_str = 'A'
    return sta_specs[s][j_str] > 0


# check if station s is compatible with date t
def is_check_airbus(j, i, airbus_check):
    return j in airbus_check[i]