from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # get instance from datasets in instance folder
    instance = get_instance()

    # get optimal scheduling for airbusses
    schedule = solve_aircraft_scheduling(instance)


if __name__ == "__main__":
    main()