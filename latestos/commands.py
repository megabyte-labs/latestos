import sys

from latestos.scraper.utils import get_os_scraper
from latestos.files.json import update_json_release_file


DEFAULT_JSON_FILENAME = "./template.json"


def main():
    """ Entry point for the script """
    # Get os_name, json_filename, bash_command from command line arguments
    os_name, json_filename, bash_command = get_params()

    # Get the scraper depending on the OS name
    scraper = get_os_scraper(os_name)

    # Get latest release data
    iso_url, checksum_url, version = scraper.get_latest_release_data()

    # Update the JSON file
    update_json_release_file(json_filename, iso_url, checksum_url, version)

    print(f"Updated {json_filename}")


def get_params() -> tuple:
    """
    Get parameters from command line 

    Returns:
        (str, str, list): os name, json filename, bash command
    """
    # If there is only one argument (script name), raise an exception
    if len(sys.argv) <= 1:
        raise ValueError(
            "You need to pass the OS name (ubuntu, centos, fedora or arch)")

    args = sys.argv[1:]

    # Extract the necessary variables
    os_name = args[0]
    json_filename = args[1] if len(args) > 1 else DEFAULT_JSON_FILENAME
    bash_command = args[2].split() if len(args) > 2 else []

    return os_name, json_filename, bash_command

if __name__ == "__main__":
    main()
