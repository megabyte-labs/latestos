import lxml.html

from latestos.scraper.mirrors import ArizonaMirror

class ArchScraper(ArizonaMirror):
    """ Latest Arch Version Checker """
    URL = "https://mirror.arizona.edu/archlinux/iso/latest/"
    OS_NAME = "Arch"

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
        return href.endswith(".iso")

    def link_is_for_iso_checksum(self, href: str) -> bool:
        """
        Checks whether a link (href) corresponds to a release iso checksum file

        Returns:
            (bool): is iso checksum file
        """
        return href == "sha1sums.txt"
    