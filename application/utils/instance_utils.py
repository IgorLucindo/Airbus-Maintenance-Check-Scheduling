# get instance from datasets in instance folder
def get_instance():
    # folder paths
    array_folder_path = "instances/arrays/"
    dict_folder_path = "instances/dictionaries/"

    # get dicts
    sta_specs = get_sta_specs_dict()
    airbusses_array = get_array_instance(array_folder_path + "airbusses.txt")

    # get sets
    A = range(len(airbusses_array)) # array
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


# get an array in a .txt file
def get_array_instance(file_path):
    with open(file_path, "r") as file:
        data = file.read()

    return eval(data)


# get a dictionary in a .txt file
def get_dictionary_instance(file_path):
    with open(file_path, "r") as file:
        data = file.read()

    return eval(data)


# get check dictionary
def get_check_set():
    total_C_checks = 10

    return {
        'A': [0],
        'Phase': range(total_C_checks)
    }