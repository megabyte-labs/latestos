from abc import ABC

import lxml.html
from lxml.html import HtmlElement

from latestos.scraper.base import BaseScraper


class ArizonaMirror(BaseScraper, ABC):
    """
    Defines common functions for latest OS scrapers using the Arizona Mirror.
    ArizonaMirror is an abstract class like BaseScraper, but it has a lot of
    functionality already defined.
    """
    URL = ""
    RELEASE_ISO_URL_SUFFIX = ""
    OS_NAME = "OS"

    def get_latest_release(self) -> tuple:
        """
        Find latest release.

        Returns:
            (HtmlElement, str): release html data, release url
        """
        # Fetch the Mirror URL
        r = self.fetch(self.__class__.URL)

        # Parse the HTML and gather all links
        document = lxml.html.fromstring(r)
        links = document.xpath(".//a")

        # Get the link that corresponds to the latest release
        latest_release_url = self.get_latest_release_url(links)

        # If the link was not found, raise error
        if not latest_release_url:
            raise Exception(
                f"Could not find latest {self.__class__.OS_NAME} release")

        # Fetch data for latest release, parse the html, then return both
        r = self.fetch(latest_release_url)
        return lxml.html.fromstring(r), latest_release_url

    def get_latest_release_url(self, mirror_links: list) -> str:
        """
        Check all mirror links and return the one that corresponds to the
        latest release.

        Returns:
            (str): latest release url
        """
        raise NotImplementedError()

    def parse_latest_release_url(self, link: HtmlElement) -> str:
        """
        Takes a link HTML element and parses the URL from it

        Returns:
            (str): parsed and formatted latest release url
        """
        url = link.xpath(".//@href")[0]
        return f'{self.__class__.URL}{url}{self.__class__.RELEASE_ISO_URL_SUFFIX}'

    def get_iso_filename_and_url(self, release: HtmlElement, release_url: str) -> tuple:
        """
        Extracts ISO filename and URL from release.

        Returns:
            (str, str): iso filename, iso url
        """
        # Get the files in the current mirror folder
        files = release.xpath(".//a")

        # Go through the files until we find the iso file
        for f in files:
            href = f.xpath("./@href")
            href = href[0] if len(href) else None

            if href and self.link_is_for_iso_file(href):
                return f.text, f"{release_url}{href}"

        raise Exception("Could not find ISO filename and URL")

    def link_is_for_iso_file(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso file

        Returns:
            (bool): is iso file
        """
        raise NotImplementedError()

    def get_iso_checksum_url(self, release: HtmlElement, iso_filename: str, release_url: str) -> str:
        """
        Extracts ISO checksum URL from release.

        Returns:
            str: checksum url
        """
        # Get the files in the current mirror folder
        files = release.xpath(".//a")

        # Go through the files until we find the iso checksum file
        for f in files:
            href = f.xpath("./@href")
            href = href[0] if len(href) else None

            if href and self.link_is_for_iso_checksum(href):
                return f"{release_url}{href}"

        raise Exception(f"Could not find {iso_filename} checksum")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        raise NotImplementedError()

    def get_iso_version(self, iso_filename: str) -> str:
        """
        Extracts ISO version from release.

        Returns:
            str: iso version
        """
        filename_sections = self.get_filename_sections(iso_filename)

        # If the filename was properly extracted, return it
        if len(filename_sections) >= 2:
            return filename_sections[1]

        raise Exception(f"Could not extract {iso_filename} OS version")

    def get_filename_sections(self, iso_filename: str) -> list:
        """
        Extracts filename data from the iso_filename.
        By default it splits by "-".

        Returns:
            (list): filename data - second element is the os version
        """
        return iso_filename.split("-")
