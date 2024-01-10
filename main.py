from visualize_output import *
from modules.district import *

def main():

    # At least 1 argument
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [desired district]")
    # Shows format output
    elif sys.argv[1] == "format":
        data = load_JSON_output("output/output-format.json")
        plot_output(data)
    # Shows output of one district between 1 - 3 
    elif sys.argv[1].isnumeric() and 1 <= int(sys.argv[1]) <= 3:
        district = District(int(sys.argv[1]), "costs-own")
        plot_output(district.return_output())
    else:
        print("Invalid input.")


if __name__ == "__main__":
    main()
