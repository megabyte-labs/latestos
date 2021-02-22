import sys
import subprocess

from latestos.scraper.utils import get_os_scraper
from latestos.files.json import update_json_release_file

from latestos.vagrantup.check import VAGRANTUP_BOX_OS_LIST, vagrantup_check


DEFAULT_JSON_FILENAME = "./template.json"


def get_latest_os():
    # Get os_name, json_filename, bash_command from command line arguments
    os_name, json_filename, bash_command = get_params()
    run(os_name, json_filename, bash_command)


def run(os_name: str,
        json_filename: str = DEFAULT_JSON_FILENAME,
        bash_command: list = []):
    """ Entry point for the script """
    # Get the scraper depending on the OS name
    scraper = get_os_scraper(os_name)

    # Get latest release data
    iso_url, checksum_url, version = scraper.get_latest_release_data()

    # Update the JSON file
    update_json_release_file(json_filename, iso_url, checksum_url, version)
    print(f"Updated {json_filename}")

    # if OS is on vagrantup box os list, check if the version is up to date
    if bash_command and os_name in VAGRANTUP_BOX_OS_LIST:
        uptodate = vagrantup_check(os_name, version)

        if not uptodate:
            run_subprocess(bash_command)


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
    bash_command = args[2:] if len(args) > 2 else []

    return os_name, json_filename, bash_command


def run_subprocess(bash_command: list, verbose: bool = True):
    """
    Runs bash command.
    """
    # Open subprocess and run
    proc = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = proc.communicate()

    # Print the output if necessary
    if verbose:
        print(output.decode("utf-8"))


if __name__ == "__main__":
    get_latest_os()
