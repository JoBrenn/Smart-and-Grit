from visualize_output import *
from modules.district import *

def main():

    district = District(int(sys.argv[1]), "costs-own")

    # json_data = load_JSON_output()
    plot_output(district.return_output())


if __name__ == "__main__":
    main()
