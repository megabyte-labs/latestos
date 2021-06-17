from abc import ABC
from typing import Any, Dict, List, Tuple


class BaseClient(ABC):
    """ Defines the interface used to make requests through the web """

    def get(self, url: str, *args, **kwargs) -> Tuple[Any, str]:
        """
        Makes a GET request to the given URL.

        Args:
            url (str): url to get

        Returns:
            (Tuple[Any, str]): response object, raw response text
        """
        raise NotImplementedError()

    def post(self, url: str, data: dict, content_type: str) -> Tuple[Any, str]:
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
        raise NotImplementedError()

    def set_cookies(self, cookies: list, url: str):
        """
        Set cookies.

        Args:
            cookies (List[Dict[str, str]]): cookies - each is a dict {name: val}
            url (str): domain's base url
        """
        raise NotImplementedError()

    def close(self):
        """
        Closes the client / ends sessions.
        """
        raise NotImplementedError()

    def restart(self):
        """
        Restarts the client
        """
        raise NotImplementedError()
