# check if x_ijst is schedulable
def is_schedulable(i, j, s, t):
    return is_station_capability(s, j) and is_date_compatible(s, t)


# check if station s has capability for check j
def is_station_capability(s, j):
    return


# check if station s is compatible with date t
def is_date_compatible(s, t):
    return