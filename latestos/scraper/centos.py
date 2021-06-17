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

            # Check if "stream"
            if "stream" not in link_version:
                continue

            version_number = link_version.replace("-stream", "") \
                                         .replace(".", "") \
                                         .replace("/", "")

            # Check if link is an OS version link (only numbers)
            if version_number.isnumeric():
                # Extract number
                release_link_number = float(version_number)

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

    def get_iso_version(self, iso_filename: str) -> str:
        """
        Extracts ISO version from release.

        Returns:
            str: iso version
        """
        filename_sections = self.get_filename_sections(iso_filename)

        # If the filename was properly extracted, return it
        if len(filename_sections) >= 4:
            major_release = filename_sections[2]
            date = filename_sections[4]
            return f"{major_release}.0.{date}"

        raise Exception(f"Could not extract {iso_filename} OS version")
