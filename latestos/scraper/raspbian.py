from latestos.scraper.mirrors import ArizonaMirror


class RaspbianScraper(ArizonaMirror):
    """
    Latest Raspbian Version Checker
    Note that this does not extract data from an Arizona Mirror
    """
    URL = "https://downloads.raspberrypi.org/rpd_x86/images/"
    OS_NAME = "Raspbian"

    def get_latest_release_url(self, mirror_links: list) -> str:
        """
        Check all mirror links and return the one that corresponds to the
        latest release.

        Returns:
            (str): latest release url
        """
        return self.parse_latest_release_url(mirror_links[-1])

    def link_is_for_iso_file(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso file

        Returns:
            (bool): is iso file
        """
        return href.endswith(".iso")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        return href.endswith(".sha1")

    def get_filename_sections(self, iso_filename: str) -> list:
        """
        Extracts filename data from the iso_filename.
        By default it splits by "-".

        Returns:
            (list): filename data - second element is the os version
        """
        sections = iso_filename.split("-raspios", 1)

        # Replace version dashes - to dots .
        version = sections[0].replace("-", ".")

        # Remember to place ISO version on second element
        return [sections[1], version]
