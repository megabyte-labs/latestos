from latestos.scraper.mirrors import ArizonaMirror

import lxml.html
from lxml.html import HtmlElement


class DebianScraper(ArizonaMirror):
    """ Latest Debian Version Checker """
    URL = "https://mirror.arizona.edu/debian-cd/current-live/amd64/iso-hybrid/"
    SHASUMS_URL = "https://mirror.arizona.edu/debian-cd/current-live/amd64/iso-hybrid/SHA1SUMS"
    OS_NAME = "Debian"

    def get_latest_release(self) -> tuple:
        """
        Gets data from mirror and then parses it (html).

        Returns:
            (HtmlElement, str): parsed html data, release url
        """
        r = self.fetch(self.__class__.URL)

        # Parse the HTML
        document = lxml.html.fromstring(r)

        return document, self.__class__.URL

    def link_is_for_iso_file(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso file

        Returns:
            (bool): is iso file
        """
        return href.endswith("amd64-standard.iso")

    def get_iso_checksum_url(self, release: HtmlElement, iso_filename: str, release_url: str) -> str:
        """
        Extracts ISO checksum URL from release.

        Returns:
            str: checksum url
        """
        return self.__class__.SHASUMS_URL

    def get_filename_sections(self, iso_filename: str) -> list:
        """
        Extracts filename data from the iso_filename.
        By default it splits by "-".

        Returns:
            (list): filename data - second element is the os version
        """
        # Ignore first element so that ISO version goes second and not third
        return iso_filename.split("-")[1:]
