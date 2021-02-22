import json


def update_json_release_file(
    json_file: str, iso_url: str, checksum_url: str, version: str):
    """
    Reads a JSON file and updates the latest OS release variables.
    """
    # Read JSON
    data = read_json_file(json_file)

    # Create the "variables" field if it doesn't exist
    has_variables_field = data.get("variables", None) != None
    if not has_variables_field:
        data["variables"] = {}

    # Update the latest OS variables
    data["variables"]["iso_url"] = iso_url
    data["variables"]["iso_checksum_url"] = checksum_url
    data["variables"]["iso_version"] = version

    # Save changes
    write_json_file(data, json_file)


def read_json_file(json_file: str) -> dict:
    """
    Reads JSON file.

    Returns:
        (dict): JSON data
    """
    try:
        # Try to read the JSON data from the file
        with open(json_file) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        # If the file does not exist, use the default template
        with open("./latestos/templates/template.json") as f:
            return json.loads(f.read())
    except Exception:
        # If there's an unexpected error, then just re-raise the exception
        raise Exception(f"Could not read {json_file}")


def write_json_file(data, json_file: str):
    """
    Saves JSON in a file.
    """
    try:
        # Try to open the file and write the json to it
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception:
        raise Exception(f"Could not write new data to {json_file}")
