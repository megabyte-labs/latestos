from latestos.scraper.mirrors import ArizonaMirror


class CentOSScraper(ArizonaMirror):
    """ Latest CentOS Version Checker """
    URL = "https://mirror.arizona.edu/centos/"
    RELEASE_ISO_URL_SUFFIX = "isos/x86_64/"
    OS_NAME = "CentOS"

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
            link_version = link.text

            # Check if link is an OS version link (only numbers)
            if link_version[:-1].isnumeric():
                # Extract number
                release_link_number = float(link_version[:-1])

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
        return href.endswith("-dvd1.iso")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        return href.endswith("CHECKSUM")
