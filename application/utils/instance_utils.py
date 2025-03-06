# get instance from datasets in instance folder
def get_instance():
    # get dicts
    sta_specs = get_sta_specs_dict()

    # get sets
    A = range(len(get_airbus_set())) # array
    C = get_check_set() # dict
    
    return [A, C, S, T, sta_specs]


# get sta_spces dictionary
def get_sta_specs_dict():
    return {
        'STA_1': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_3': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_5': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_6': {'AC': 2, 'P': 2, 'STATION_CAP': 2},
        'STA_8': {'AC': 1, 'P': 0, 'STATION_CAP': 1},
        'STA_9': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_11': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_12': {'AC': 2, 'P': 2, 'STATION_CAP': 2},
        'STA_13': {'AC': 1, 'P': 1, 'STATION_CAP': 1},
        'STA_14': {'AC': 1, 'P': 0, 'STATION_CAP': 1},
        'STA_15': {'AC': 1, 'P': 0, 'STATION_CAP': 1},
        'STA_16': {'AC': 1, 'P': 1, 'STATION_CAP': 1}
    }


# get aircraft_dictionary_checks_count dictionary
def get_airbus_set():
    file_path = "instances/dictionaries/aircraft_dictionary_checks_count.txt"

    with open(file_path, "r") as file:
        data = file.read()

    return eval(data)


# get check dictionary
def get_check_set():
    return {
        'A': [0],
        'Phase': range(10)
    }