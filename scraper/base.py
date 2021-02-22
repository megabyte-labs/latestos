from abc import ABC

import requests
from lxml.html import HtmlElement


class BaseScraper(ABC):
    """
    BaseScraper is an abstract class, which means it can not be used by itself.
    It defines common functionality amongst all latest OS scrapers.
    One must override all non implemented methods and the URL variable.
    """
    # Root URL of the mirror
    URL = None

    def fetch(self, url: str = None) -> str:
        """
        Fetches data from an url, defaults to the mirror's root URL.

        Returns:
            (str): response text
        """
        if url:
            r = requests.get(url)
        else:
            r = requests.get(self.__class__.URL)
        return r.text

    def get_latest_release_data(self) -> tuple:
        """
        Gets latest OS release data.

        Returns:
            (str, str, str): iso url, checksum url, os version
        """
        # Get latest release
        release, release_url = self.get_latest_release()

        # Extract data from latest release
        filename, iso_url = self.get_iso_filename_and_url(release, release_url)
        checksum_url = self.get_iso_checksum_url(release, filename, release_url)
        version = self.get_iso_version(filename)

        return iso_url, checksum_url, version

    def get_latest_release(self) -> tuple:
        """
        Find latest release.

        Returns:
            (HtmlElement, str): release html data, release url
        """
        raise NotImplementedError()

    def get_iso_filename_and_url(self, release: HtmlElement, release_url: str) -> tuple:
        """
        Extracts ISO filename and URL from release.

        Returns:
            (str, str): iso filename, iso url
        """
        raise NotImplementedError()

    def get_iso_checksum_url(self, release: HtmlElement, iso_filename: str, release_url: str) -> str:
        """
        Extracts ISO checksum URL from release.

        Returns:
            str: checksum url
        """
        raise NotImplementedError()

    def get_iso_version(self, iso_filename: str, release_url: str) -> str:
        """
        Extracts ISO version from release.

        Returns:
            str: iso version
        """
        raise NotImplementedError()
