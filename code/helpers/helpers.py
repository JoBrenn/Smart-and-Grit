import json

def write_output_to_JSON(data: list, file_name: str, district_number: int) -> None:
    """Write data to output JSON file in output/."""
    # Craft file path
    file_path = f"output/JSON/{file_name}-district_{district_number}-output.json"

    # Open file path in WRITE mode and write data
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)
