from latestos.scraper.mirrors import ArizonaMirror


class FedoraScraper(ArizonaMirror):
    """ Latest Fedora Version Checker """
    URL = "https://mirror.arizona.edu/fedora/linux/releases/"
    RELEASE_ISO_URL_SUFFIX = "Server/x86_64/iso/"
    OS_NAME = "Fedora"

    def get_latest_release_url(self, mirror_links: list) -> str:
        """
        Check all mirror links and return the one that corresponds to the
        latest release.

        Returns:
            (str): latest release url
        """
        latest_release_number, latest_release_url = 0, None

        # Go through mirror links
        for link in mirror_links:
            # Check if link is an OS version link (only numbers)
            if link.text[:-1].isnumeric():
                # Extract number
                release_link_number = float(link.text[:-1])

                # Update latest release if necessary
                if release_link_number > latest_release_number:
                    latest_release_number = release_link_number
                    latest_release_url = self.parse_latest_release_url(link)

        return latest_release_url

    def link_is_for_iso_file(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso file

        Returns:
            (bool): is iso file
        """
        return href.startswith("Fedora-Server-dvd") and href.endswith(".iso")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        return href.endswith("CHECKSUM")

    def get_filename_sections(self, iso_filename: str) -> list:
        """
        Extracts filename data from the iso_filename.

        Returns:
            (list): filename data - second element is the os version
        """
        # Split filename
        arch = "x86_64-"
        sections = iso_filename.split(arch)

        if len(sections) >= 1:
            # Format the version before returning it
            version = sections[1].replace(".iso", "").replace("-", ".")
            sections = [sections[0], version]

        return sections
