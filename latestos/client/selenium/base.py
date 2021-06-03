from abc import ABC
from typing import Any, Dict, List, Optional, Tuple
from latestos.client.base import BaseClient


BROWSER_TIMEOUT = 60


class SeleniumClient(BaseClient, ABC):
    """
    Uses selenium and a selenium driver.
    """
    headers = {}
    timeout = None if BROWSER_TIMEOUT == 0 else BROWSER_TIMEOUT

    def __init__(self) -> None:
        super().__init__()
        self.setup_options()
        self.init_browser()

    def setup_options(self) -> None:
        """
        Setup driver options. Must be overriden.
        """
        raise NotImplementedError()

    def init_browser(self) -> None:
        """
        Initilizes a browser instance.
        """
        raise NotImplementedError()

    def get(self, url: str, *args, **kwargs) -> Tuple[Any, str]:
        """
        Makes a GET request to the given URL.

        Args:
            url (str): url to get

        Returns:
            (Tuple[Any, str]): response object, raw response text
        """
        self.driver.get(url)

        # Get the HTML content of the website
        html_source = self.driver.page_source

        if kwargs.get("json", False):
            # If json data is expected, return raw data and parsed json
            parsed_json = self._parse_json_data(html_source)
            return None, parsed_json
        else:
            return None, html_source

        return None, html_source

    def post(
        self,
        url: str,
        data: dict,
        content_type: Optional[str] = None
    ) -> Tuple[Any, str]:
        """
        Makes a POST request to the given URL.

        Args:
            url (str): url to post to
            data (dict): data to send
            content_type (str): content type of the request

        Returns:
            (Tuple[Any, str]): response object, raw response text
        """
        raise NotImplementedError()

    def get_cookies(self) -> List[Dict[str, str]]:
        """
        Get cookies in use.

        Returns:
            (List[Dict[str, str]]): cookies - each of 'em is a dict {name: val}
        """
        cookies = self.driver.get_cookies()
        formatted_cookies = [{c.get("name"): c.get("value")} for c in cookies]
        return formatted_cookies

    def set_cookies(self, cookies: list, url: str):
        """
        Set cookies.

        Args:
            cookies (List[Dict[str, str]]): cookies - each is a dict {name: val}
            url (str): domain's base url
        """
        for cookie in cookies:
            cookie_data = cookie.items()
            for cookie_name, cookie_val in cookie_data:
                self.driver.add_cookie({
                    "name": cookie_name,
                    "value": cookie_val,
                    "domain": url
                })

    def close(self) -> None:
        """
        Closes the client / ends sessions.
        """
        self.driver.close()
        self.driver.quit()

    def restart(self):
        """
        Restarts the client
        """
        self.close()
        self.init_browser()

    def _get_page_source(self, *args) -> str:
        """
        Get the raw page source.

        Returns:
            (str): html page source
        """
        try:
            return self.driver.page_source
        except Exception:
            return ""
