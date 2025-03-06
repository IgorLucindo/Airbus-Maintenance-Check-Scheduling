from utils.check_schedulability_utils import *
from itertools import product
from datetime import datetime
import csv
import re


# get instance from datasets in instance folder
def get_instance(total_days):
    # set variables
    initial_date = "2023-11-04"

    # folder paths
    array_folder_path = "instances/arrays/"
    dict_folder_path = "instances/dictionaries/"
    dataset_folder_path = "instances/datasets/"

    # get dicts
    sta_specs = get_sta_specs_dict() # station
    airbus_subfleet = get_dictionary_instance(dict_folder_path + "aircraft_TAIL_SUBFLEET.txt") # airbus
    # airbus_subfleet = get_keys_to_int(airbus_subfleet) # airbus (int version)
    station_airbus_date = get_dictionary_instance(dict_folder_path + "station_availability_dict.txt")
    station_airbus_date = get_keys_to_int(station_airbus_date)
    station_airbus_date = dict_date_to_int(station_airbus_date, initial_date) # station date
    airbus_check = get_dictionary_instance(dict_folder_path + "aircraft_dictionary_checks_specific.txt") # airbus check
    # airbus_check = get_keys_to_int(airbus_check)
    # airbus_check = dict_check_to_int(airbus_check) # airbus check (int version)
    check_days = gets_maximum_interval(dataset_folder_path + "check_specs.csv") # check
    # check_days = get_keys_to_int(check_days) # check (int version)
    check_daytogo = get_dictionary_instance(dict_folder_path + "days_to_go_dict.txt")
    # check_daytogo = get_keys_to_int(check_daytogo)
    # check_daytogo = dict_check_to_int(check_daytogo) # airbus check (int version)

    # get sets
    A = get_array_instance(array_folder_path + "unique_fleet.txt") # array
    # A = range(len(A)) # array (int version)
    C = get_check_set() # array
    S = range(len(sta_specs)) # array
    T = range(total_days) # array
    S_ijt = get_S_ijt(A, C, S, T, airbus_subfleet, station_airbus_date, sta_specs) # dict
    
    return [A, C, S, S_ijt, T, sta_specs, airbus_check, check_days, check_daytogo]


# get sta_spces dictionary
def get_sta_specs_dict():
    return {
        0: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        1: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        2: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        3: {'A': 2, 'P': 2, 'STATION_CAP': 2},
        4: {'A': 1, 'P': 0, 'STATION_CAP': 1},
        5: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        6: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        7: {'A': 2, 'P': 2, 'STATION_CAP': 2},
        8: {'A': 1, 'P': 1, 'STATION_CAP': 1},
        9: {'A': 1, 'P': 0, 'STATION_CAP': 1},
        10: {'A': 1, 'P': 0, 'STATION_CAP': 1},
        11: {'A': 1, 'P': 1, 'STATION_CAP': 1}
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


def get_keys_to_int(data):
    return {i: value for i, value in enumerate(data.values())}


def dict_date_to_int(data, initial_date):
    reference_date = datetime.strptime(initial_date, '%Y-%m-%d')

    # Transform dates into integers
    new_data = {}
    for station, dates in data.items():
        new_data[station] = {
            (datetime.strptime(date, '%Y-%m-%d') - reference_date).days: planes
            for date, planes in dates.items()
        }

    return new_data


def get_check_set():
    return ['A', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10']

def get_S_ijt(A, C, S, T, airbus_subfleet, station_airbus_date, sta_specs):
    S_ijt = {}
    for i, j, s, t in product(A, C, S, T):
        if is_station_airbus_date(i, s, t, airbus_subfleet, station_airbus_date) and is_station_check(s, j, sta_specs):
            if i not in S_ijt:
                S_ijt[i] = {}
            if j not in S_ijt[i]:
                S_ijt[i][j] = {}
            if t not in S_ijt[i][j]:
                S_ijt[i][j][t] = [s]
            else:
                S_ijt[i][j][t].append(s)

    return S_ijt


def dict_check_to_int(data):
    def map_check(check):
        if check.startswith('A'):
            return 0
        elif check.startswith('C'):
            # Extract numeric part and convert to integer
            return int(check[1:])  # Assuming C02 becomes 2, C03 becomes 3, etc.
        return check  # For other cases (if needed)

    return {key: [map_check(value) for value in values] for key, values in data.items()}


# get check days dictionary
def gets_maximum_interval(filepath):
    # Initialize with A as a single key
    check_days = {'A': None}

    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row['FLEET'].startswith('AIRBUS'):
                continue  # Skip rows that are not from AIRBUS
            
            check_name = row['Check']
            days = int(row['Days'])

            # Check if it's an A-check or C-check
            if check_name.startswith('A'):
                if check_days['A'] is None or days < check_days['A']:  
                    check_days['A'] = days  # Store the shortest interval for A-checks
            elif check_name.startswith('P'):
                if '-' in check_name:  # Expand ranges (e.g., C01-C06)
                    start, end = map(lambda x: int(re.search(r'\d+', x).group()), check_name.split('-'))
                    for i in range(start, end + 1):
                        key = f"{'C'}{i:02d}"  # Ensure formatting (C01, C02, etc.)
                        check_days[key] = days
                else:
                    check_days[check_name] = days  # Single C check

    return check_days