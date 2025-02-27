from utils.instance_utils import *
from utils.model_utils import *


def main():
    # get instance from datasets in instance folder
    instance = get_instance()

    run_model(instance)

if __name__ == "__main__":
    main()