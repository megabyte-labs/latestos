import requests

import lxml.html

VAGRANTUP_BOX_URL = "https://app.vagrantup.com/ProfessorManhattan/"

VAGRANTUP_BOX_OS_LIST = [
    "ubuntu",
    "arch"
]


def vagrantup_check(os_name: str, version: str) -> bool:
    """
    Checks whether an OS is on version :version on the vagrantup box.

    Returns:
        (bool): is OS updated?
    """
    # Fetch url & parse HTML
    r = requests.get(VAGRANTUP_BOX_URL)
    document = lxml.html.fromstring(r.text)

    # Get list of boxes titles, each in the ":os-name :version" format
    boxes = document.xpath(".//h4")

    # Go through each box
    for box in boxes:
        # Format box title
        formatd_box = " ".join(box.xpath("string()").replace("\n", "").split())

        # Extract OS name & version
        box_os_name, box_os_version = get_os_data_from_box_title(formatd_box)

        # if current box corresponds to the os we're looking for, check if
        # os version is up to date
        if os_name in box_os_name.lower():
            if version in box_os_version:
                # Do a final check for the version
                v_nums = box_os_version.replace(version, "").replace(".", "")

                if not v_nums or (v_nums.isnumeric() and int(v_nums) == 0):
                    return True

    return False


def get_os_data_from_box_title(box_title: str) -> tuple:
    """
    Gets OS name and version from a properly formatted box title.

    Returns:
        (str, str): OS name, OS version
    """
    # Split box title into [os name, os version]
    box_title_elements = box_title.split(" v")

    return box_title_elements[0], box_title_elements[1]
