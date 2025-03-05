# check if x_ijst is schedulable
def is_schedulable(i, j, s, t):
    return is_station_check(s, j) and is_station_airbus(s, i) and is_station_date(s, t) and is_check_airbus(j, i)


# check if station s has capability for check j
def is_station_check(s, j):
    return


# check if station s is compatible with airbus i
def is_station_airbus(s, i):
    return


# check if station s is compatible with date t
def is_station_date(s, t):
    return


# check if station s is compatible with date t
def is_check_airbus(j, i):
    return