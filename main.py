from visualize_output import *
from modules.district import *

def main():
    json_data = load_JSON_output(sys.argv[1])
    plot_output(json_data)



if __name__ == "__main__":
    main()
