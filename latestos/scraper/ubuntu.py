from latestos.scraper.mirrors import ArizonaMirror


class UbuntuScraper(ArizonaMirror):
    """ Latest Ubuntu Version Checker """
    URL = "https://mirror.arizona.edu/ubuntu-releases/"
    OS_NAME = "Ubuntu"

    def get_latest_release_url(self, mirror_links: list) -> str:
        """
        Check all mirror links and return the one that corresponds to the
        latest release.

        Returns:
            (str): latest release url
        """
        latest_release_url = None

        # Go through mirror links
        for link in mirror_links:
            # Parse link
            link_version = link.text
            dotless_link = link_version[:-1].replace(".", "")

            # If link is an OS version link (only numbers), update release url
            if dotless_link.isnumeric():
                latest_release_url = self.parse_latest_release_url(link)

        return latest_release_url

    def link_is_for_iso_file(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso file

        Returns:
            (bool): is iso file
        """
        return href.endswith("server-amd64.iso")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        return href == "SHA256SUMS"
