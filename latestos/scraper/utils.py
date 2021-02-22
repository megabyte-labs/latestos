from latestos.scraper.base import BaseScraper
from latestos.scraper.arch import ArchScraper
from latestos.scraper.centos import CentOSScraper
from latestos.scraper.fedora import FedoraScraper
from latestos.scraper.ubuntu import UbuntuScraper


def get_os_scraper(os_name: str) -> BaseScraper:
    """
    Takes an OS name and returns the corresponding scraper.

    Returns:
        (BaseScraper): scraper
    """
    os_name = os_name.lower()

    if os_name == "arch":
        return ArchScraper()
    elif os_name == "centos":
        return CentOSScraper()
    elif os_name == "fedora":
        return FedoraScraper()
    elif os_name == "ubuntu":
        return UbuntuScraper()
    else:
        raise ValueError(f"{os_name}")
