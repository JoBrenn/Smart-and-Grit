import json

def write_output_to_JSON(data: list, file_name: str, district_number: int) -> None:
    """Write data to output JSON file in output/."""
    # Craft file path
    file_path = f"output/JSON/{file_name}-district_{district_number}-output.json"

    # Open file path in WRITE mode and write data
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)

def print_helpmsg():
    print("Methods:")
    print("  --help:\t\t Display help manual")
    print("  --format:\t\t Display formatted output")
    print("  --h[isto[gram]]:\t Get histogram of N runs of random assignment Manhattan distance algorithm.")
    print("  --randrwalk:\t\t Randomly assigns houses to batteries. " + \
                        "Creates cable path through randomly taking random steps until destination is reached.")
    print("  --randmanh:\t\t Randomly assigns houses to batteries. \t\t\t\t(Manhattan Distance)")
    print("  --greedmanh:\t\t Uses greedy algorithm to assign houses to batteries. \t\t(Manhattan Distance)")
    print("  --greedmanhcap:\t Uses greedy algorithm to assign houses to capped batteries. \t(Manhattan Distance) ")
    print("  exit:\t Stop running main.")
    print()

def get_method_input() -> str:
    method = ""
    while not method:
        method = input("Specify method: ")
        if method in ["h", "-h", "help", "--help"]:
            print_helpmsg()
            method = ""
    return method

def get_district_input() -> int:
    district = 0
    while not district:
        district = int(input("Specify district number: "))
        # print("input:", district)
        if not 1 <= district <= 3:
            print("Try again.")
            district = 0

    return district
